import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load CSV
df = pd.read_csv("data/training_sample.csv")

# 🔥 FIX FOR YOUR ERROR
df.columns = df.columns.str.strip()               # remove spaces
df.columns = df.columns.str.replace("\ufeff", "") # remove hidden BOM

print("Columns in CSV:", df.columns.tolist())     # debug print

# Now training
vect = TfidfVectorizer()
X = vect.fit_transform(df["text"])
y = df["label"]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, "model/model.pkl")
joblib.dump(vect, "model/vectorizer.pkl")

print("Model trained successfully!")
