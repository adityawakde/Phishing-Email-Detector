import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Sample dataset (we will later replace with real dataset)
data = {
    "text": [
        "urgent click here to verify account",
        "your bank account is suspended login immediately",
        "hello friend how are you",
        "meeting scheduled for tomorrow",
        "update your password now",
        "let's catch up soon"
    ],
    "label": [1, 1, 0, 0, 1, 0]  # 1 = phishing, 0 = safe
}

df = pd.DataFrame(data)

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.3, random_state=42
)

vectorizer = TfidfVectorizer()
X_train_vec = vectorizer.fit_transform(X_train)

model = LogisticRegression()
model.fit(X_train_vec, y_train)

# Save model + vectorizer
joblib.dump(model, "ml_model/phishing_model.pkl")
joblib.dump(vectorizer, "ml_model/vectorizer.pkl")

print("Model trained and saved successfully!")