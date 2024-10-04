from core.logger import Logger
from typing import Any
import discord
from core.config_reader import ConfigReader, Configuration
from core.text_ai_message import TextAiMessage

class Pama(discord.Client):
    def __init__(self, *, intents: discord.Intents, cfg: Configuration, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.__logger = Logger("Pama")
        self.__ollama = TextAiMessage(cfg)

    async def on_ready(self):
        self.__logger.info(f'Logged in as {self.user}!')

    async def on_message(self, message):
        self.__logger.info(f'Message from {message.author.name}: {message.content}')
        response = await self.__ollama.get_ollama_message(message.content, f"@{message.author.name}")
        
        await message.channel.send(response)
        

def main():
    logger = Logger("main")
    cfg_reader = ConfigReader("config.json")
    cfg = cfg_reader.read_config()
    
    intents = discord.Intents.default()
    intents.message_content = True

    client = Pama(intents=intents, cfg=cfg)
    logger.info("Successfully started")
    client.run(cfg.discord_token, log_level=0)

if __name__ == "__main__":
    main()