"""Tests for coscientist/framework.py - API key validation and config."""

import pytest

try:
    from coscientist.framework import validate_api_keys

    HAS_FRAMEWORK = True
except (ImportError, Exception):
    HAS_FRAMEWORK = False

pytestmark = pytest.mark.skipif(
    not HAS_FRAMEWORK,
    reason="Framework dependencies not available (langchain-google-genai, etc.)",
)


class TestValidateApiKeys:
    """Tests for API key validation at startup."""

    def test_missing_openai_key_raises(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.setenv("TAVILY_API_KEY", "test-tavily-key")
        with pytest.raises(EnvironmentError, match="OPENAI_API_KEY"):
            validate_api_keys()

    def test_missing_tavily_key_raises(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        monkeypatch.delenv("TAVILY_API_KEY", raising=False)
        with pytest.raises(EnvironmentError, match="TAVILY_API_KEY"):
            validate_api_keys()

    def test_missing_both_required_raises(self, monkeypatch):
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        monkeypatch.delenv("TAVILY_API_KEY", raising=False)
        with pytest.raises(EnvironmentError, match="Missing required API keys"):
            validate_api_keys()

    def test_all_required_present_succeeds(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        monkeypatch.setenv("TAVILY_API_KEY", "test-tavily-key")
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")
        monkeypatch.setenv("GOOGLE_API_KEY", "test-google-key")
        warnings = validate_api_keys()
        assert len(warnings) == 0

    def test_missing_optional_returns_warnings(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
        monkeypatch.setenv("TAVILY_API_KEY", "test-tavily-key")
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        warnings = validate_api_keys()
        assert len(warnings) == 2
