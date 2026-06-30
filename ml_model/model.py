import joblib

model = joblib.load("ml_model/phishing_model.pkl")
vectorizer = joblib.load("ml_model/vectorizer.pkl")


def predict_email(text: str):
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]

    if prediction == 1:
        return "Phishing"
    else:
        return "Safe"