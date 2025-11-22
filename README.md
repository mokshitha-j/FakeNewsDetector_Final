# FakeNewsDetector_Final
Fake news detector (Hybrid model)
Fake News Detector – Multilingual, ML-Powered (Streamlit Web App)
This project detects Fake or Real news using a hybrid approach that combines rule-based NLP, multilingual processing, and Machine Learning classification.
It supports multiple Indian languages using langdetect and deep-translator, and provides a credibility score along with explanation and user feedback logging.

🚀 Features

Multilingual input support (English, Hindi, Kannada, Tamil, Telugu)

Automatic language detection

Auto-translation to English for ML processing

Text cleaning & preprocessing

ML-based prediction using TF-IDF + Logistic Regression

Highlighting suspicious keywords

Credibility scoring

User feedback system (Like/Dislike)

Simple Streamlit UI

Training script included

📁 Project Structure
FakeNewsDetector_Final/
│
├── app.py                    # Main Streamlit application
├── train_model.py            # Script used to train ML model
├── requirements.txt          # Required Python libraries
│
├── model.pkl                 # Trained logistic regression model
├── vectorizer.pkl            # TF-IDF vectorizer
│
├── data/
│   ├── training_sample.csv   # Sample training dataset
│   ├── feedback.csv          # Feedback storage file
│
└── modules/
    └── feedback_handler.py   # Functions to save & read feedback

🔧 Installation
1. Clone this repository
git clone https://github.com/mokshitha-j/FakeNewsDetector_Final.git
cd FakeNewsDetector_Final

2. Install required libraries
pip install -r requirements.txt

▶️ Run the Application

Run this command:

streamlit run app.py


Your browser will open the Fake News Detector UI.

🧠 How It Works (Pipeline)

User Input
→ Enter any news headline or text.(from trained data set)

Text Pre-processing
→ Language detection
→ Translation (if not English)
→ Text cleaning

Machine Learning Prediction
→ TF-IDF vectorization
→ Logistic Regression classification

Credibility Scoring
→ Keyword checks
→ Model confidence score
→ Dataset similarity check

Output Displayed
→ Real / Fake
→ Credibility score
→ Highlighted risky keywords
→ Explanation
→ User feedback buttons

📊 Training the Model

If you want to retrain the model:

python train_model.py


This will regenerate:

model.pkl

vectorizer.pkl

🙋‍♂️ User Feedback System

Feedback is stored in:

data/feedback.csv


It helps analyze how users perceive model correctness.

⚠️ Notes

Make sure feedback.csv and training_sample.csv remain inside the data/ folder.

Do NOT upload private datasets or API keys.

You may replace training_sample.csv with your own dataset to improve accuracy.

