import joblib

# Load trained model + vectorizer
model = joblib.load("ml_model/phishing_model.pkl")
vectorizer = joblib.load("ml_model/vectorizer.pkl")


def predict_email(text: str):
    """
    Predict if email is phishing or safe using ML model.
    """

    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec)[0].max()

    label = "Phishing" if prediction == 1 else "Safe"

    return {
        "label": label,
        "confidence": float(round(probability * 100, 2))
    }