from google import genai
from google.genai import types

from app.config.settings import settings
from app.llm.client import LlmClient


class GeminiLlmClient(LlmClient):

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    async def generate(self, messages: list[dict]) -> str:

        system_instruction = None
        contents = []

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "system":
                system_instruction = content

            elif role == "user":
                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_text(text=content)
                        ],
                    )
                )

            elif role == "assistant":
                contents.append(
                    types.Content(
                        role="model",
                        parts=[
                            types.Part.from_text(text=content)
                        ],
                    )
                )

        response = await self.client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
            ),
        )

        return response.text