import csv
import os

FEEDBACK_FILE = "data/feedback.csv"

def init_feedback_db():
    """Initialize CSV file if it doesn’t exist."""
    if not os.path.exists(FEEDBACK_FILE):
        os.makedirs(os.path.dirname(FEEDBACK_FILE), exist_ok=True)
        with open(FEEDBACK_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["news_id", "name", "feedback", "comment"])

def save_feedback(news_id, name, feedback, comment=""):
    """Save a feedback entry to CSV."""
    init_feedback_db()
    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([news_id, name, feedback, comment])

def get_feedback_summary(news_id):
    """Return total likes/dislikes and names for a news_id."""
    likes = 0
    dislikes = 0
    like_names = []
    dislike_names = []

    if not os.path.exists(FEEDBACK_FILE):
        return likes, dislikes, like_names, dislike_names

    # Open CSV safely, replacing bad characters
    with open(FEEDBACK_FILE, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("news_id") == news_id:
                if row.get("feedback") == "like":
                    likes += 1
                    like_names.append(row.get("name", "Unknown"))
                elif row.get("feedback") == "dislike":
                    dislikes += 1
                    dislike_names.append(row.get("name", "Unknown"))
    return likes, dislikes, like_names, dislike_names

