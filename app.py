from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import onnxruntime as ort
import cv2
import base64

app = Flask(__name__)
CORS(app)

@app.route("/solve", methods = ["POST"])
def solve():
    try:
        data = request.get_json(force = True)

        if not data or "image" not in data:
            return jsonify({"error": "Missing 'image' in JSON payload"}), 400

        image_data = data["image"]
        _, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        np_arr = np.frombuffer(image_bytes, np.uint8)

        img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        img = cv2.convertScaleAbs(img, alpha = 1.5, beta = -50)
        img = cv2.GaussianBlur(img, (3, 3), 0)

        _, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        height, width = binary.shape[:2]
        binary = cv2.resize(binary, (width * 3, height * 3), interpolation = cv2.INTER_CUBIC)
        binary = cv2.bitwise_not(binary)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        binary = cv2.dilate(binary, kernel, iterations = 1)
        binary = cv2.GaussianBlur(binary, (3, 3), 0)

        _, final = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        contours, _ = cv2.findContours(final, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)

            if w * h < 100: 
                continue

            boxes.append((x, y, w, h))

        boxes = sorted(boxes, key = lambda b: b[0])
        letter_images = []

        for (x, y, w, h) in boxes:
            letter = final[y:y + h, x:x + w]
            padding = 8
            letter = cv2.copyMakeBorder(letter, padding, padding, padding, padding, cv2.BORDER_CONSTANT, value = 0)
            h, w = letter.shape
            size = max(w, h)
            square = np.zeros((size, size), dtype = np.uint8)

            x_offset = (size - w) // 2
            y_offset = (size - h) // 2

            square[y_offset:y_offset + h, x_offset:x_offset + w] = letter
            square = cv2.resize(square, (28, 28), interpolation = cv2.INTER_AREA)

            letter_images.append(square)

        session = ort.InferenceSession("model/emnist_cnn.onnx")
        input_name = session.get_inputs()[0].name
        output_name = session.get_outputs()[0].name
        mapping = {}

        with open("model/emnist_mapping.txt") as f:
            for line in f:
                label, ascii_code = line.strip().split()
                mapping[int(label)] = chr(int(ascii_code))

        def preprocess_letter(img):
            img = cv2.resize(img, (28, 28))
            img = img / 255.0
            img = img.astype(np.float32)
            img = np.expand_dims(img, axis = 0)
            img = np.expand_dims(img, axis = 0)

            return img

        def predict_letter(img):
            img = preprocess_letter(img)
            output = session.run([output_name], {input_name: img})[0]
            pred = np.argmax(output, axis = 1)[0]

            return mapping[pred]

        result = ""

        for _, letter in enumerate(letter_images):
            char = predict_letter(letter)
            result += char

        return jsonify({"text": result})
    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run()