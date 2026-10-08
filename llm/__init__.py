"""Unified LLM provider layer. Rules never pretend to be an LLM; provider_used is reported."""
from .provider import LLMProvider, LLMUnavailable, load_provider
__all__=["LLMProvider","LLMUnavailable","load_provider"]
