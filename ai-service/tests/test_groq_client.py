import pytest
import json
from services.groq_client import GroqClient, GroqClientError, FALLBACK_DESCRIBE, FALLBACK_RECOMMEND

class MockMessage:
    def __init__(self, content):
        self.content = content

class MockChoice:
    def __init__(self, message):
        self.message = message

class MockCompletion:
    def __init__(self, content):
        self.choices = [MockChoice(MockMessage(content))]

class MockChat:
    def __init__(self, completions_mock):
        self.completions = completions_mock

class MockCompletions:
    def __init__(self, success=True, content="{}", error=None):
        self.success = success
        self.content = content
        self.error = error
        
    def create(self, **kwargs):
        if not self.success:
            raise self.error or Exception("Mocked API Error")
        return MockCompletion(self.content)

class MockGroq:
    def __init__(self, success=True, content="{}", error=None):
        self.chat = MockChat(MockCompletions(success, content, error))

@pytest.fixture
def mock_groq_success(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test_key")
    client = GroqClient()
    client.client = MockGroq(success=True, content='{"title": "Test Title", "description": "Test Desc", "severity": "High", "impact": "Test Impact"}')
    return client

@pytest.fixture
def mock_groq_failure(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test_key")
    client = GroqClient()
    client.client = MockGroq(success=False)
    # We reduce the tenacious retry times for tests to make them fast
    # but since tenacity decorators are applied at import time, 
    # we just let it use the fallback
    return client

def test_generate_description_success(mock_groq_success):
    result = mock_groq_success.generate_description("system", "user")
    assert result['title'] == "Test Title"
    assert result['severity'] == "High"

def test_generate_description_fallback_on_api_error(mock_groq_failure, monkeypatch):
    # Shorten retry waits for test
    monkeypatch.setattr("tenacity.wait_exponential.__call__", lambda self, retry_state: 0.1)
    
    result = mock_groq_failure.generate_description("system", "user")
    assert result == FALLBACK_DESCRIBE

def test_generate_description_fallback_on_invalid_json(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test_key")
    client = GroqClient()
    client.client = MockGroq(success=True, content='Invalid JSON')
    
    result = client.generate_description("system", "user")
    assert result == FALLBACK_DESCRIBE
