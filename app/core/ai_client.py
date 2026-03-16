from openai import AsyncOpenAI

from app.core.config import settings

ai_client = AsyncOpenAI(
    api_key=settings.QWEN_API_KEY,
    base_url=settings.QWEN_BASE_URL,
)
