# AI Service - Penetration Test Manager

This microservice provides AI-driven capabilities for the Penetration Test Manager using the Groq API (LLaMA-3.3-70b). It is built with Flask 3.x and Python 3.11.

## Features
- AI-powered vulnerability description, recommendation, and report generation.
- Strict JSON output using prompt engineering.
- Robust error handling with retries, exponential backoff, and safe fallback responses.
- Security middleware with prompt injection detection and HTML stripping.
- Rate limiting (30 req/min per IP).

## Setup

1. **Clone the repository.**
2. **Set Environment Variables:**
   Copy `.env.example` to `.env` and fill in your `GROQ_API_KEY`.
   ```bash
   cp .env.example .env
   ```

## Running Locally

### Using Docker (Recommended)
```bash
docker-compose up --build
```
The service will be available at `http://localhost:5000`.

### Without Docker
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```

## API Endpoints

### `GET /health`
Returns the health status of the service.

### `POST /describe`
Generates a structured description for a vulnerability.
- **Payload:** `{"vulnerability": "SQL Injection in login page"}`

### `POST /recommend`
Generates remediation recommendations.
- **Payload:** `{"vulnerability": "SQL Injection"}`

### `POST /generate-report`
Generates a full report from a list of findings.
- **Payload:** `{"input_data": "Found a SQL injection vulnerability in the Banking Application authentication module"}`

## Running Tests
Run the test suite using pytest:
```bash
pytest -v
```
All Groq API calls are mocked during testing, so no network or API key is required.

## Integration Notes
- This service must be run alongside the Spring Boot backend.
- The backend should communicate with this service over `http://ai-service:5000` (in a shared Docker network) or `http://localhost:5000` if running standalone.
- In case of AI failure, the service returns a `200 OK` with a fallback JSON response. Always handle the JSON payload according to the predefined schemas.
