from pathlib import Path
import joblib

MODEL_PATH = Path("models/news_classifier.joblib")

class NLPDetector:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Model not found. Run `python train_model.py` before starting the app."
            )
        self.model = joblib.load(MODEL_PATH)

    def predict(self, text: str) -> dict:
        text = (text or "").strip()
        if not text:
            raise ValueError("Please enter some text to verify.")

        probabilities = self.model.predict_proba([text])[0]
        classes = list(self.model.classes_)
        probability_by_class = {
            str(label): float(probabilities[i]) for i, label in enumerate(classes)
        }
        predicted = str(self.model.predict([text])[0])
        fake_probability = probability_by_class.get("fake", 0.0)
        authentic_probability = probability_by_class.get("authentic", 0.0)

        return {
            "label": predicted,
            "fake_probability": fake_probability,
            "authentic_probability": authentic_probability,
            "probabilities": probability_by_class,
        }
