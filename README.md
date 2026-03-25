# SIMKULIAH Login Bot OCR API

API service for solving **SIMKULIAH** login CAPTCHA using OCR. This API receives a CAPTCHA image (Base64) and returns the recognized text using an OCR pipeline built with **OpenCV** and **ddddocr**.

## Requirements

- Python 3.10+
- Virtual environment

## Installation

```bash
# Clone repository
git clone https://github.com/naufalhanif25/simkuliah-login-bot-api.git
cd simkuliah-login-bot-api

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

After running locally, the API will be available at:
`http://localhost:5000`

## Deployment

The API has been deployed and is publicly accessible at:

`https://simkuliah-login-bot-api.vercel.app/`

## API Endpoint

### Solve CAPTCHA

Solve **SIMKULIAH** CAPTCHA using OCR.

**Endpoint:**

```
POST /solve
```

**Full URL (Deployed):**

```
https://simkuliah-login-bot-api.vercel.app/solve
```

### Request Format

The API expects a JSON request containing a Base64 encoded image.

```json
{
    "image": "data:image/png;base64,iVBORw0KGgoAAAANS..."
}
```

### Response Format

#### Success

```json
{
    "text": "ABCDE"
}
```

#### Error

```json
{
    "error": "Missing 'image' in JSON payload"
}
```

---

## Notes

* The API was initially designed specifically for **SIMKULIAH** CAPTCHA format, but has since been extended to support other CAPTCHA types.
* Accuracy depends on the complexity of the CAPTCHA, model capabilities, and pre-processing flow.
* Intended for automation and educational purposes.