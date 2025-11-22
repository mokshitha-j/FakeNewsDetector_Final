import streamlit as st
import joblib
import re
import hashlib
import pandas as pd
from langdetect import detect
from deep_translator import GoogleTranslator
from modules.feedback_handler import save_feedback, get_feedback_summary

# -------------------------
# Fake news keywords: Multi-language
# -------------------------
FAKE_KEYWORDS = {
    "en": ["fake", "shocking", "unbelievable", "click this link", "died", "accident", "free"],
    "hi": ["असत्य", "झूठ", "फर्जी", "अविश्वसनीय"],
    "kn": ["ಸುಳ್ಳು", "ಅಸತ್ಯ", "ಮಿಥ್ಯಾ"],
    "ta": ["வதந்தி", "பொய்", "சத்தியமில்லாதது"],
    "te": ["అసత్యం", "మోసం", "తప్పు"]
}

# -------------------------
# Utility Functions
# -------------------------
def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s\u0900-\u097F\u0B80-\u0BFF\u0C80-\u0CFF\u0C00-\u0C7F]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        if lang.startswith("hi"): return "hi"
        elif lang.startswith("kn"): return "kn"
        elif lang.startswith("ta"): return "ta"
        elif lang.startswith("te"): return "te"
        return "en"
    except:
        return "en"

def highlight_keywords(text: str) -> str:
    lang = detect_language(text)
    keywords = FAKE_KEYWORDS.get(lang, [])
    highlighted = text
    for kw in keywords:
        highlighted = re.sub(kw, f"<mark>{kw}</mark>", highlighted, flags=re.IGNORECASE)
    return highlighted

def translate_to_english(text: str) -> str:
    try:
        lang = detect(text)
        if lang != "en":
            return GoogleTranslator(source="auto", target="en").translate(text)
        return text
    except:
        return text

def get_news_id(news_text: str) -> str:
    return hashlib.md5(news_text.encode("utf-8")).hexdigest()

# -------------------------
# NEW: Load Training Dataset
# -------------------------
TRAINING_DATA = pd.read_csv("data/training_sample.csv")

def is_in_dataset(text: str) -> bool:
    cleaned_input = clean_text(text)
    for row in TRAINING_DATA["text"]:
        if clean_text(str(row)) == cleaned_input:
            return True
    return False

# -------------------------
# Explanation Generator
# -------------------------
def generate_explanation(text, label, score, keywords):
    lang = detect_language(text)
    explanation = f"**Detected Language:** {lang}\n\n"

    if keywords:
        explanation += f"**Keywords Detected:** {', '.join(keywords)}\n\n"
    # ❌ REMOVED THE "Keywords Detected: None" LINE COMPLETELY

    if label == "Unpredictable":
        explanation += (
            "**Reason:** This text does not match any known training data. "
            "Hence model cannot validate it correctly.\n"
            "> Default confidence (50%) applied.\n"
        )
        return explanation

    if label == "Fake":
        explanation += (
            "**Reason for Fake:**\n"
            "- Contains patterns similar to misinformation.\n"
            "- May include misleading tone or context.\n"
            "- ML model low credibility score.\n"
        )
    else:
        explanation += (
            "**Reason for Real:**\n"
            "- No fake-indicator keywords detected.\n"
            "- Matches patterns of verified real news in training data.\n"
            "- ML model high confidence.\n"
        )

    explanation += f"\n**Final Confidence Score:** {score}%"
    return explanation

# -------------------------
# Load ML Model
# -------------------------
@st.cache_resource
def load_model():
    try:
        model = joblib.load("model/model.pkl")
        vectorizer = joblib.load("model/vectorizer.pkl")
        return model, vectorizer
    except:
        return None, None

model, vectorizer = load_model()

# -------------------------
# Streamlit UI
# -------------------------
st.title("Fake News Detector")
st.write("Enter a news statement to check whether it may be Real or Fake. Supports multiple languages.")

# Session State
if 'current_news_text' not in st.session_state:
    st.session_state.current_news_text = ""

if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = ("", 0)

if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = False

news_text_input = st.text_area("News Text", height=150)

# -------------------------
# Analyze Button
# -------------------------
if st.button("Analyze"):
    if not news_text_input.strip():
        st.warning("Please enter some text.")
        st.stop()

    st.session_state.current_news_text = news_text_input
    cleaned = clean_text(news_text_input)
    news_id = get_news_id(news_text_input)

    # -------------------------
    # PREDICTION LOGIC
    # -------------------------

    if model is None or vectorizer is None:
        lang = detect_language(news_text_input)
        keywords = FAKE_KEYWORDS.get(lang, [])
        score = 50
        for word in keywords:
            if word in news_text_input:
                score -= 10
        label = "Fake" if score < 50 else "Real"

    else:
        if not is_in_dataset(news_text_input):
            label = "Unpredictable"
            score = 50
        else:
            vec = vectorizer.transform([cleaned])
            pred = model.predict(vec)[0]
            score = 80 if pred == 1 else 35
            label = "Real" if pred == 1 else "Fake"

    st.session_state.prediction_result = (label, score)
    st.session_state.feedback_submitted = False

# -------------------------
# Display Results
# -------------------------
news_text = st.session_state.current_news_text
label, score = st.session_state.prediction_result

if news_text:
    st.subheader("Prediction: " + label)
    st.write("Credibility Score:", score)

    st.subheader("Original Text:")
    highlighted = highlight_keywords(news_text)
    st.write(highlighted, unsafe_allow_html=True)

    translated = translate_to_english(news_text)
    if translated != news_text:
        st.subheader("Translated Text (English):")
        st.write(translated)

    lang = detect_language(news_text)
    detected_keywords = [kw for kw in FAKE_KEYWORDS.get(lang, []) if kw in news_text]

    st.subheader("Explanation:")
    explanation = generate_explanation(news_text, label, score, detected_keywords)
    st.write(explanation)

# -------------------------
# Feedback Section
# -------------------------
# -------------------------
# Feedback Section (Only show AFTER analysis)
# -------------------------

if news_text:  # <-- ADDED THIS CONDITION
    news_id = get_news_id(news_text)
    likes, dislikes, like_names, dislike_names = get_feedback_summary(news_id)

    if not st.session_state.feedback_submitted:
        user_name = st.text_input("Enter your name to submit feedback:", key="feedback_name")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("✅ Like", key="like_btn"):
                if user_name.strip():
                    save_feedback(news_id, user_name, "like", "")
                    st.success(f"Thanks {user_name}! Your feedback has been recorded.")
                    st.session_state.feedback_submitted = True
                else:
                    st.warning("Please enter your name.")

        with col2:
            if st.button("❌ Dislike", key="dislike_btn"):
                if user_name.strip():
                    save_feedback(news_id, user_name, "dislike", "")
                    st.success(f"Thanks {user_name}! Your feedback has been recorded.")
                    st.session_state.feedback_submitted = True
                else:
                    st.warning("Please enter your name.")

    likes, dislikes, like_names, dislike_names = get_feedback_summary(news_id)
    total_feedback = likes + dislikes

    if total_feedback > 0:
        st.subheader(f"Feedback ({total_feedback} given)")
        st.write(f"👍 Likes: {likes} — {like_names}")
        st.write(f"👎 Dislikes: {dislikes} — {dislike_names}")

