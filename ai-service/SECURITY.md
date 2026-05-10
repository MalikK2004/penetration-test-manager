# Security Documentation

## Threat Model
This service acts as an intermediary between the Spring Boot backend and the Groq LLM API.
- **Threat 1: Prompt Injection:** Malicious users may attempt to bypass instructions to output harmful content or leak system prompts.
- **Threat 2: XSS/HTML Injection:** Payloads may contain raw HTML intended to render maliciously on the frontend.
- **Threat 3: Denial of Service (DoS):** Flooding the API with requests, exhausting the Groq API limits.
- **Threat 4: AI Failure/Timeout:** The Groq API may become unresponsive, leading to application crashes.

## Mitigations Implemented

### 1. Prompt Injection Sanitization
All inputs are checked against a regex of known prompt injection phrases (e.g., "ignore previous instructions", "bypass safety"). If a match is found, the request is immediately rejected with an HTTP 400.

### 2. HTML Stripping
The `bleach` library is used to strip all HTML tags and attributes from incoming requests before they reach the LLM, preventing XSS payloads from being reflected in the output.

### 3. Rate Limiting
`Flask-Limiter` is implemented with a strict limit of 30 requests per minute per IP to prevent abuse and API quota exhaustion.

### 4. Robust Fallback Strategy
`tenacity` is used for 3 retries with exponential backoff on Groq API calls. If all retries fail, or if an invalid JSON response is returned, the service degrades gracefully and returns a predefined, safe fallback JSON response instead of crashing or returning a 500 error.

### 5. Secure Headers
The application automatically sets secure headers (Content-Security-Policy, X-Content-Type-Options, Strict-Transport-Security, etc.) on every response.

## Testing Performed
- Unit tests verifying HTML stripping and prompt injection detection.
- Mocks verifying the fallback behavior upon API failure.
- Successful endpoint request handling.

## Residual Risks
- **Zero-Day Prompt Injections:** The current injection detection is regex-based and may not catch novel, sophisticated prompt injection attacks. Continual updating of the `INJECTION_PATTERNS` list is required.
- **Rate Limit Bypass:** The current rate limiter uses an in-memory store. For a multi-node production setup, Redis should be configured as the storage backend for `Flask-Limiter`.
