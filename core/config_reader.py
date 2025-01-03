from dataclasses import dataclass
import json

from core.logger import Logger, Severity

@dataclass
class Configuration:
    """
    Configuration from config.json
    """
    ollama_model: str
    ollama_url: str
    discord_token: str
    use_modern_emojis: bool
    allow_fake_sql_injection: bool
    max_stored_messages: int


class ConfigReader:
    def __init__(self, file_name: str) -> None:
        self.__file = file_name
        self.__logger = Logger("ConfigReader")
        
    def read_config(self) -> Configuration:
        """Reads the config.json

        Returns:
            Configuration: all settings of the config.json that is required
        """
        try:
            file_buffer = open(self.__file, "r")
            
            output_json = json.load(file_buffer)
            
            config = Configuration(
                ollama_model=output_json["ollamaModel"], 
                ollama_url=output_json["ollamaUrl"], 
                discord_token=output_json["discordToken"], 
                use_modern_emojis=output_json["useModernEmojis"],
                allow_fake_sql_injection=output_json["allowFakeSQLInjection"],
                max_stored_messages=output_json["maxStoredMessages"]
            )
            
            return config
        except FileNotFoundError as e:
            self.__logger.error(f"Could not find '{self.__file}': {str(e)}", severity=Severity.HIGH)
            exit(1)
        except json.JSONDecodeError as e:
            self.__logger.error(f"Could not read '{self.__file}': {str(e)}", severity=Severity.HIGH)
            exit(1)
        except KeyError as ke:
            self.__logger.error(f"Configuration error: {str(ke)} Please make sure it's a correct json format and that '{str(ke)}' has been set", severity=Severity.HIGH)
            exit(1)
        except ValueError as ve:
            self.__logger.error(f"Invalid setting in '{self.__file}': {str(ve)}", severity=Severity.HIGH)
            exit(1)
        except Exception as e:
            self.__logger.error(f"Unknown error: {str(e)}", severity=Severity.HIGH)
            exit(1)