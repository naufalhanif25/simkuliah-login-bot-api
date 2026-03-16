from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2
import ddddocr
import cv_image
import normal_text
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
        image = cv_image.Image(image = img)
        image.apply(cv2.convertScaleAbs, alpha = 1.5, beta = -50)
        _, binary = cv2.threshold(image(), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        image.replace(binary)

        height, width = image.shape()
        image.apply(cv2.resize, (width * 3, height * 3), interpolation = cv2.INTER_LANCZOS4)
        image.apply(cv2.bilateralFilter, 9, 75, 75)
        image.apply(cv2.morphologyEx, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
        image.apply(cv2.GaussianBlur, (3, 3), 0)

        image.apply(cv2.filter2D, -1, np.array([
            [0, -1, 0],
            [-1, 5,-1],
            [0, -1, 0]
        ]))

        coords = np.column_stack(np.where(image() > 0))
        angle = cv2.minAreaRect(coords)[-1]
        angle = -(90 + angle) if angle < -45 else -angle
        height, width = image.shape()
        matrix = cv2.getRotationMatrix2D((width // 2, height // 2), angle, 1.0)
        image.apply(cv2.warpAffine, matrix, (width, height), flags = cv2.INTER_CUBIC, borderMode = cv2.BORDER_REPLICATE)

        normal = normal_text.NormalText()
        ocr = ddddocr.DdddOcr(show_ad = False)
        text = ocr.classification(image())
        text = normal.normalize(text)

        return jsonify({"text": text})
    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run()