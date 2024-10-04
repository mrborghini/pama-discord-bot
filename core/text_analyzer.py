from core.config_reader import Configuration
from core.text_ai_message import TextAiMessage
from mediapipe.tasks import python
from mediapipe.tasks.python import text

class TextAnalyzer(TextAiMessage):
    def __init__(self, cfg: Configuration) -> None:
        super().__init__(cfg)
        self.__model_path = "bert_classifier.tflite"
        
        base_options = python.BaseOptions(model_asset_path=self.__model_path)
        options = text.TextClassifierOptions(base_options=base_options)
        self.classifier = text.TextClassifier.create_from_options(options)
    
    def find_matching_emoji(result: float):
        pass

    async def get_ai_message(self, message: str, author: str):
        return await self.get_ollama_message(message, author)
    
    def __convert_to_percentage(self, score: float):
        return int(score * 100)

    async def detect_message_tone(self, message: str):
        classification_result = self.classifier.classify(message)

        detections = classification_result.classifications[0].categories

        for detection in detections:
            if detection.category_name == "negative":
                score_percentage = self.__convert_to_percentage(detection.score)
                return f"That message was {score_percentage}% {detection.category_name}"