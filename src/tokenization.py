import os
import pickle
import shutil

from sklearn.feature_extraction.text import CountVectorizer
from util.database import connect_database, upload_model, download_model


def fit_tokenizer(df):
    cv = CountVectorizer(max_features=2500)
    cv.fit(df['Resume'])
    if not os.path.isdir("./saved"):
        os.mkdir("saved")
    filename = os.path.join("saved", "tokenizer.sav")
    with open(filename, "wb") as file:
        pickle.dump(cv, file)
    shutil.make_archive("tokenizer", "zip", "saved")
    connection = connect_database()
    upload_model(connection, "tokenizer", "tokenizer.zip", 0)
    connection.close()


def load_tokenizer():
    connection = connect_database()
    download_model(connection, "tokenizer", "tokenizer_loaded.zip", 0)
    os.makedirs("tokenizer_loaded")
    shutil.unpack_archive("tokenizer_loaded.zip", "tokenizer_loaded", "zip")
    with open(os.path.join("tokenizer_loaded", "tokenizer.sav"), "rb") as file:
        cv = pickle.load(file)
    return cv


def tokenize_dataset(df, tokenizer=None):
    if tokenizer is None:
        cv = load_tokenizer()
    else:
        cv = tokenizer
    x = cv.transform(df['Resume']).toarray()
    y = df['Category']
    return x, y
