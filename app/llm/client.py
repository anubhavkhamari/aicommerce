from abc import ABC, abstractmethod

class LlmClient(ABC) :
    @abstractmethod
    async def generate(self, messages: list[dict])->str:
        pass
