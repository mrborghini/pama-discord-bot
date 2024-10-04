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
    
    def find_matching_emoji(self, percentage: int) -> str:
        if 0 <= percentage <= 10:
            return ":D"  # Happy
        elif 11 <= percentage <= 20:
            return ":)"  # Slightly happy
        elif 21 <= percentage <= 30:
            return ":|"  # Neutral
        elif 31 <= percentage <= 40:
            return ":("  # Slightly sad
        elif 41 <= percentage <= 50:
            return ">:("  # Angry
        elif 51 <= percentage <= 60:
            return ">:|"  # More angry
        elif 61 <= percentage <= 70:
            return ">:O"  # Very angry
        elif 71 <= percentage <= 80:
            return "X("  # Extremely angry
        elif 81 <= percentage <= 90:
            return "X[!"  # Outraged
        elif 91 <= percentage <= 100:
            return "XX(!!"  # Furious
        else:
            return "Invalid percentage"

    async def get_ai_message(self, message: str, author: str):
        return await self.get_ollama_message(message, author)
    
    def __convert_to_percentage(self, score: float):
        return int(score * 100)
    
    def __classify_message(self, message: str):
        classification_result = self.classifier.classify(message)

        detections = classification_result.classifications[0].categories
        return detections
    
    def get_negative_percentage(self, message: str):
        detections = self.__classify_message(message)
        for detection in detections:
            if detection.category_name == "negative":
                score_percentage = self.__convert_to_percentage(detection.score)
                return (score_percentage, detection.category_name)

    async def detect_message_tone(self, message: str):
        percentage, category = self.get_negative_percentage(message)
        return f"That message was {percentage}% {category}"
    
    async def get_ollama_message_tone(self, message: str, author: str, user_id: int):
        message = await self.get_ollama_message(message, author)
        percentage, _ = self.get_negative_percentage(message)
        # Replace the username with the user id
        message = message.replace(author, f"<@{user_id}>")
        return f"{message} {self.find_matching_emoji(percentage)}"