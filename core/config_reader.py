import json


class Configuration:
    """
    Configuration from config.json
    """
    ollama_model: str
    ollama_url: str
    discord_token: str

class ConfigReader:
    def __init__(self, file_name: str) -> None:
        self.__file = file_name
        
    def read_config(self) -> Configuration:
        """Reads the config.json

        Returns:
            Configuration: all settings of the config.json that is required
        """
        try:
            file_buffer = open(self.__file, "r")
            
            output_json = json.load(file_buffer)
            
            config = Configuration()
            
            config.discord_token = output_json["discordToken"]
            config.ollama_model = output_json["ollamaModel"]
            config.ollama_url = output_json["ollamaUrl"]
            
            return config
        except Exception as e:
            pass