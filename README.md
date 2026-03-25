# SIMKULIAH Login Bot OCR API

API service for solving **SIMKULIAH** login CAPTCHA using OCR.
This API receives a CAPTCHA image (Base64) and returns the recognized text using an OCR pipeline built with **OpenCV** and **ddddocr**

## Requirements

- Python 3.10+
- Virtual environment

## Installation

```bash
# Clone repository
git clone https://github.com/<user>/simkuliah-login-bot-api.git
cd simkuliah-login-bot-api

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

After running, the API will be available at:
`http://localhost:5000`

## API Endpoint

### Solve CAPTCHA

Solve **SIMKULIAH** CAPTCHA using OCR.

`POST /solve`

The API expects a JSON request containing a Base64 encoded image.

```json
{ "image": "data:image/png;base64,iVBORw0KGgoAAAANS..." }
```

The API will provide a response like this if the request is successful

```json
{ "text": "ABCDE" }
```

and like this if error.

```json
{ "error": "Missing 'image' in JSON payload" }
```

## Notes

- The API is designed specifically for **SIMKULIAH** CAPTCHA format.
- Accuracy depends on the CAPTCHA complexity and preprocessing pipeline.
- Intended for automation and educational purposes.
