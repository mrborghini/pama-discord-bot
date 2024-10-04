import json

import httpx

from core.config_reader import Configuration
from core.logger import Logger, Severity

class OllamaMessage:
    content: str
    author: str

class Conversation:
    messages: list[OllamaMessage]
    
    def __init__(self) -> None:
        self.messages = []
    
    def add_message(self, content: str, author: str):
        new_message = OllamaMessage()
        new_message.author = author
        new_message.content = content
        self.messages.append(new_message)
        
    def to_dict(self):
        return [{"author": message.author, "content": message.content} for message in self.messages]
    
    def to_string(self):
        return "\n".join(f"{message.author}: {message.content}" for message in self.messages)

class TextAiMessage:
    def __init__(self, cfg: Configuration) -> None:
        self.__base_url = cfg.ollama_url
        self.__ollama_model = cfg.ollama_model
        self.__conversation_file = "conversation.json"
        self.__system_message_file = "system_message.txt"
        self.conversation: Conversation
        self.__logger = Logger("TextAiMessage")
        
    def get_system_message(self):
        try:
            with open(self.__system_message_file, "r") as f:
                return f.read()
        except FileNotFoundError as e:
            self.__logger.error(f"Could not find {self.__system_message_file}: {str(e)}", severity=Severity.HIGH)
            return "You are now Pama from minecraft story mode"
    
    def load_conversation(self) -> Conversation:
        try:
            with open(self.__conversation_file, "r") as f:
                out_json = json.load(f)
                
                self.conversation = Conversation()
                
                for ollama_message in out_json:
                    self.conversation.add_message(ollama_message["content"], ollama_message["author"])
        except FileNotFoundError as e:
            self.__logger.warning(f"Conversation file doesn't exist {str(e)}", severity=Severity.LOW)
            self.conversation = Conversation()
    
    def save_conversation(self):
        with open(self.__conversation_file, "w") as f:
            json.dump(self.conversation.to_dict(), f, indent=4)

    async def get_ollama_message(self, message: str, author: str) -> str:
        self.load_conversation()
        self.conversation.add_message(message, author)
        async with httpx.AsyncClient() as client:
            content = {
                "system": self.get_system_message(),
                "model": self.__ollama_model,
                "stream": False,
                "prompt": self.conversation.to_string()
            }
            try:
                response = await client.post(f"{self.__base_url}/api/generate", json=content, timeout=None)
                
                text_message = response.json()
                
                self.conversation.add_message(text_message["response"], "Pama")
                
                self.save_conversation()
                
                return text_message["response"]
            except Exception as e:
                self.__logger.error(str(e))
                return "Something went wrong 😭"