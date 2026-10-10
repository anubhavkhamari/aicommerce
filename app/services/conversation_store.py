from collections import defaultdict
from threading import Lock

class ConversationStore : 
    def __init__(self) : 
        self._messages = defaultdict(list)
        self._lock = Lock()

    def get_messages(self, conversation_id: str) -> list[dict] :
        with self._lock : 
            return list(self._messages[conversation_id])
        
    def add_message(
            self,
            conversation_id,
            role: str,
            content: str
    ) -> None :
        with self._lock :
            self._messages[conversation_id].append(
                {
                    "role" : role,
                    "content" : content,
                }
            )

conversation_store = ConversationStore();