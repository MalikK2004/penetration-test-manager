import os
import json
import time
from typing import Dict, Any, Optional
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from utils.logger import get_logger

logger = get_logger(__name__)

# Fallback responses
FALLBACK_DESCRIBE = {
    "title": "Service Unavailable",
    "details": "The AI service is currently unavailable. Please try again later."
}

FALLBACK_RECOMMEND = {
    "title": "Service Unavailable",
    "severity": "UNKNOWN"
}

FALLBACK_REPORT = {
    "project_name": "Service Unavailable",
    "finding": "AI generation failed. Please refer to raw findings for details."
}

class GroqClientError(Exception):
    pass

class GroqClient:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            logger.warning("GROQ_API_KEY not set. API calls will fail.")
            self.client = None
        else:
            self.client = Groq(api_key=api_key, timeout=10.0, max_retries=0) # using tenacity instead
            
        self.model = "llama-3.3-70b-versatile"
        self.total_requests = 0
        self.total_response_time = 0.0

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception),
        reraise=True
    )
    def _make_request(self, system_prompt: str, user_prompt: str) -> str:
        if not self.client:
            raise GroqClientError("Groq client not initialized (missing API key)")
            
        start_time = time.time()
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
                model=self.model,
                response_format={"type": "json_object"},
            )
            duration = time.time() - start_time
            self.total_requests += 1
            self.total_response_time += duration
            logger.info(f"Groq API call successful. Duration: {duration:.2f}s")
            return chat_completion.choices[0].message.content
        except Exception as e:
            duration = time.time() - start_time
            self.total_requests += 1
            self.total_response_time += duration
            logger.error(f"Groq API call failed after {duration:.2f}s: {str(e)}")
            raise GroqClientError(f"API request failed: {str(e)}") from e

    def get_average_response_time(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return round(self.total_response_time / self.total_requests, 2)

    def _parse_json(self, text: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
        try:
            if not text:
                logger.error("Empty response from AI")
                return fallback
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {str(e)}\nResponse: {text}")
            return fallback

    def generate_description(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        try:
            response_text = self._make_request(system_prompt, user_prompt)
            return self._parse_json(response_text, FALLBACK_DESCRIBE)
        except Exception as e:
            logger.error(f"Generate description failed completely: {str(e)}")
            return FALLBACK_DESCRIBE

    def generate_recommendation(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        try:
            response_text = self._make_request(system_prompt, user_prompt)
            return self._parse_json(response_text, FALLBACK_RECOMMEND)
        except Exception as e:
            logger.error(f"Generate recommendation failed completely: {str(e)}")
            return FALLBACK_RECOMMEND

    def generate_report(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        try:
            response_text = self._make_request(system_prompt, user_prompt)
            return self._parse_json(response_text, FALLBACK_REPORT)
        except Exception as e:
            logger.error(f"Generate report failed completely: {str(e)}")
            return FALLBACK_REPORT
