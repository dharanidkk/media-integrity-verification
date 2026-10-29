from pathlib import Path
import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

DATA_PATH = Path("data/sample_news.csv")
MODEL_PATH = Path("models/news_classifier.joblib")

def main():
    data = pd.read_csv(DATA_PATH)
    required = {"text", "label"}
    if not required.issubset(data.columns):
        raise ValueError("CSV must contain columns named 'text' and 'label'.")
    data = data.dropna(subset=["text", "label"])
    data["text"] = data["text"].astype(str)
    data["label"] = data["label"].astype(str).str.lower().str.strip()

    if set(data["label"].unique()) != {"authentic", "fake"}:
        raise ValueError("Dataset labels must be exactly 'authentic' and 'fake'.")
    if data["label"].value_counts().min() < 2:
        raise ValueError("At least two examples per class are required.")

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
    model.fit(data["text"], data["label"])

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    print(f"Training examples: {len(data)}")
    print("WARNING: bundled sample data is illustrative only; do not use its results as research evidence.")

if __name__ == "__main__":
    main()
