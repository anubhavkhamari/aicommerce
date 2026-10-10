from google import genai
from google.genai import types

from app.config.settings import settings
from app.llm.client import LlmClient
from app.tools.product_tools import search_products_tool, AVAILABLE_TOOLS

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
                            types.Part.from_text(
                                text=content
                            )
                        ],
                    )
                )

            elif role == "assistant":
                contents.append(
                    types.Content(
                        role="model",
                        parts=[
                            types.Part.from_text(
                                text=content
                            )
                        ],
                    )
                )

        tool = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name=search_products_tool["name"],
                    description=search_products_tool["description"],
                    parameters=search_products_tool["parameters"]
                )
            ]
        )

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[tool]
        )

        for _ in range(4):
            response = await self.client.aio.models.generate_content(
                model=settings.gemini_model,
                contents=contents,
                config=config
            )

            function_calls = response.function_calls or []

            if not function_calls:
                if response.text:
                    return response.text
                raise RuntimeError(
                    "Gemini returned neither text nor a function call."
                )
            
            model_content = response.candidates[0].content
            contents.append(model_content)

            for call in function_calls:
                name = call.name
                args = call.args or {}

                function = AVAILABLE_TOOLS.get(name)

                if function is None: 
                    result = {"error": "Unknown/unauthorised tool request."}
                else:
                    try:
                        if not isinstance(args, dict):
                            raise ValueError("Tool arguments must be an object.")
                        
                        result = {
                            "output": function(**args)
                        }
                    except (TypeError, ValueError) as exc:
                        result = {"error": str(exc)}
                    except Exception:
                        result = {"error": "Tool execution failed."}

                contents.append(
                    types.Content(
                        role="tool",
                        parts=[
                            types.Part.from_function_response(
                                name=name,
                                response=result
                            )
                        ]
                    )
                )

        raise RuntimeError("Maximum tool-calling iterations exceeded.")