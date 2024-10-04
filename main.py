from core.health_check import HealthCheck
from core.logger import Logger
from typing import Any
import discord
from core.config_reader import ConfigReader, Configuration
from core.text_analyzer import TextAnalyzer

class Pama(discord.Client):
    def __init__(self, *, intents: discord.Intents, cfg: Configuration, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.__logger = Logger("Pama")
        self.__ollama = TextAnalyzer(cfg)
        self.__bot_id: int
        self.__health = HealthCheck()

    async def on_ready(self):
        self.__bot_id = self.user.id
        await self.__health.check_and_fix()
        self.__logger.info(f'Logged in as {self.user}!')

    async def on_message(self, message):
        if message.author.id == self.__bot_id:
            return
        self.__logger.info(f'Message from {message.author.name}: {message.content}')
        response = await self.__ollama.get_ollama_message_tone(message.content, f"@{message.author.name}", message.author.id)
        
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