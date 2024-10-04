import os

import httpx

from core.logger import Logger, Severity


class HealthCheck:
    def __init__(self) -> None:
        self.__logger = Logger("HealthCheck")
        self.model_file = "bert_classifier.tflite"
    
    async def check_and_fix(self):
        if not os.path.isfile(self.model_file):
            await self.download_model()
    

    async def download_model(self):
        url = "https://storage.googleapis.com/mediapipe-models/text_classifier/bert_classifier/float32/latest/bert_classifier.tflite"
        try:
            self.__logger.info("Downloading Mediapipe model...")
            async with httpx.AsyncClient() as client:
                r = await client.get(url)
                r.raise_for_status()  # Ensure request was successful
                
                # Write the content to a file
                with open(self.model_file, "wb") as f:
                    f.write(r.content)
            self.__logger.info(f"Successfully downloaded model '{self.model_file}'")
        except Exception as e:
            self.__logger.error(f"Could not download Mediapipe model: '{str(e)}'", severity=Severity.HIGH)