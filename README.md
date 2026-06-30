# AI-Powered Phishing Email Detector

An intelligent phishing email detection platform developed using Python and Machine Learning. The project combines rule-based analysis with a machine learning classifier to detect phishing emails and expose the detection engine through a FastAPI REST API. A Chrome extension is included for quick email analysis.

---

# Overview

Phishing emails remain one of the most common cyberattacks targeting individuals and organizations. This project aims to improve phishing detection by combining traditional security rules with machine learning techniques.

The platform analyzes email content, calculates a phishing score, predicts whether an email is legitimate or phishing, and produces a final hybrid verdict.

---

# Features

## Rule-Based Detection

- Suspicious keyword detection
- Phishing score calculation
- URL pattern detection
- Email classification
  - Safe
  - Suspicious
  - Highly Suspicious

### Suspicious Keywords

- urgent
- verify account
- click here
- password
- bank
- login immediately

---

## Machine Learning Detection

The machine learning engine includes:

- TF-IDF Vectorization
- Logistic Regression Classifier
- Confidence Score Prediction
- Real phishing email dataset for training

---

## Hybrid Detection Engine

The final result combines:

- Rule-based analysis
- Machine learning prediction
- Basic email header analysis

This approach improves detection reliability compared to using either technique independently.

---

# Technology Stack

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

## Machine Learning

- Scikit-learn
- TF-IDF Vectorizer
- Logistic Regression
- Joblib

## Browser Extension

- HTML
- CSS
- JavaScript
- Chrome Extension API

## Development Tools

- Git
- GitHub
- Visual Studio Code

---

# Project Architecture

```
                    User
                      │
                      ▼
            Chrome Extension
                      │
                      ▼
              FastAPI REST API
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
 Rule-Based Engine         Machine Learning
          │                       │
          └───────────┬───────────┘
                      ▼
             Hybrid Detection
                      │
                      ▼
              Detection Result
```

---

# Project Structure

```
PhishingEmailDetector/
│
├── api.py
├── Procfile
├── README.md
├── requirements.txt
├── setup.py
│
├── phishing_detector/
│   ├── detector.py
│   ├── cli.py
│   └── __init__.py
│
├── ml_model/
│   ├── train.py
│   ├── train_real.py
│   ├── predict.py
│   ├── hybrid.py
│   ├── header_analyzer.py
│   ├── email_parser.py
│   ├── phishing_model.pkl
│   └── vectorizer.pkl
│
├── chrome_extension/
│
├── dataset/
│
└── tests/
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/adityawakde/PhishingEmailDetector.git
```

Navigate to the project

```bash
cd PhishingEmailDetector
```

Create a virtual environment

```bash
python3 -m venv venv
```

Activate the virtual environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the API

Start the FastAPI server

```bash
uvicorn api:app --reload
```

Open the Swagger documentation

```
http://127.0.0.1:8000/docs
```

---

# API

## Analyze Email

**Endpoint**

```
POST /analyze-hybrid
```

### Request

```json
{
    "text": "URGENT! Verify your bank account immediately."
}
```

### Example Response

```json
{
    "final_verdict": "HIGHLY SUSPICIOUS",
    "hybrid_score": 11.88,
    "headers": {},
    "ml": {
        "label": "Phishing",
        "confidence": 97.54
    },
    "rules": {
        "score": 7,
        "classification": "Highly Suspicious"
    }
}
```

---

# Chrome Extension

The Chrome extension currently supports:

- Manual email text input
- Communication with the FastAPI backend
- Instant phishing analysis
- Hybrid detection results

---

# Current Project Status

| Module | Status |
|----------|--------|
| Rule-Based Detection | ✅ Completed |
| Machine Learning Model | ✅ Completed |
| Hybrid Detection Engine | ✅ Completed |
| FastAPI REST API | ✅ Completed |
| API Documentation (Swagger) | ✅ Completed |
| Chrome Extension | ✅ Completed |
| Cloud Deployment | 🔄 In Progress |
| React Dashboard | ⏳ Planned |
| Database Integration | ⏳ Planned |
| Gmail Scanner | ⏳ Planned |
| Enterprise Email Security Features | ⏳ Planned |

---

# Roadmap

## Version 1.0

- Rule-based phishing detection
- Machine learning model
- Hybrid detection engine
- FastAPI REST API
- Chrome extension

## Version 1.1

- Deploy API on Render
- Public REST API
- Production configuration

## Version 1.2

- Database integration
- Scan history
- React dashboard

## Version 1.3

- Gmail integration
- Automatic email scanning
- Improved browser extension

## Version 2.0

- SPF validation
- DKIM validation
- DMARC analysis
- URL reputation analysis
- Docker support
- CI/CD pipeline

---

# Future Improvements

- Multiple machine learning models
- Deep learning-based phishing detection
- Attachment scanning
- Domain reputation analysis
- Threat intelligence integration
- Real-time monitoring dashboard

---

# Author

Aditya Wakde

---

# License

This project is intended for educational purposes and cybersecurity research. It should only be used in authorized environments and for ethical security testing.