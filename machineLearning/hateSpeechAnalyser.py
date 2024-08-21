import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import string
nltk.download('stopwords')
from core import *


def clean_text(text, stemmer, stopword):
    text = str(text).lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    text = [word for word in text.split() if word not in stopword]
    text = " ".join(text)
    text = [stemmer.stem(word) for word in text.split()]
    return " ".join(text)

def train_and_predict(csv_file_path, test_data):
    
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print(f"Error: The file {csv_file_path} was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file {csv_file_path} is empty.")
        return None

    df['labels'] = df['class'].map({
        0: "Hate speech detected",
        1: "Offensive language detected",
        2: "No hate and offensive speech"
    })

    df = df[['tweet', 'labels']]

    stemmer = SnowballStemmer("english")
    stopword = set(stopwords.words('english'))

    df["tweet"] = df["tweet"].apply(lambda x: clean_text(x, stemmer, stopword))

    x = np.array(df["tweet"])
    y = np.array(df["labels"])

    cv = CountVectorizer()
    x = cv.fit_transform(x)

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    print("Model Evaluation:")
    print(classification_report(y_test, y_pred))

    
    try:
        df = cv.transform([test_data]).toarray()
        prediction = clf.predict(df)[0]
    except ValueError as e:
        print(f"Error during prediction: {e}")
        return None

    return prediction

def main():
    csv_file_path = "./csv/train.csv"
    test_data = "why are you so bad man just stop your work"
    
    prediction = train_and_predict(csv_file_path, test_data)
    
    if prediction is not None:
        print(f"Prediction for the input '{test_data}': {prediction}")
    else:
        print("An error occurred during prediction.")

if __name__ == "__main__":
    main()