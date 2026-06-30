import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print("🚀 Loading dataset...")

# Load dataset
df = pd.read_csv("dataset/phishing_email.csv")

# Keep only useful columns
df = df[["Email Text", "Email Type"]].dropna()

df.columns = ["text", "label"]

print("📊 Raw labels example:")
print(df["label"].value_counts().head())

# Convert labels into binary classification
def convert_label(label):
    label = label.lower()
    if "safe" in label:
        return 0
    else:
        return 1   # phishing/spam

df["label"] = df["label"].apply(convert_label)

print("📊 Final label distribution:")
print(df["label"].value_counts())

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    df["text"],
    df["label"],
    test_size=0.2,
    random_state=42
)

# Convert text → numbers
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)

# Train model
model = LogisticRegression(max_iter=300)

print("🧠 Training ML model...")
model.fit(X_train_vec, y_train)

# Save model
joblib.dump(model, "ml_model/phishing_model.pkl")
joblib.dump(vectorizer, "ml_model/vectorizer.pkl")

print("✅ MODEL TRAINED SUCCESSFULLY ON REAL DATASET")
