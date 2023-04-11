import pandas as pd
import os
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from util.database import connect_database, save_dataset, download_dataset, save_classes


def convert_to_lower_case(df):
    df['Resume'] = df['Resume'].apply(lambda x: x.lower())


def remove_short_words(df):
    res = []
    for i in range(len(df)):
        lw = []
        for j in df['Resume'][i].split():
            if len(j) >= 3:
                lw.append(j)

        res.append(" ".join(lw))
    df["Resume"] = res


def remove_punctuations(df):
    ps = list(";?.:!,")
    for p in ps:
        df['Resume'] = df['Resume'].str.replace(p, '')
    df['Resume'] = df['Resume'].str.replace("    ", " ")
    df['Resume'] = df['Resume'].str.replace('"', '')
    df['Resume'] = df['Resume'].apply(lambda x: x.replace('\t', ' '))
    df['Resume'] = df['Resume'].str.replace("'s", "")
    df['Resume'] = df['Resume'].apply(lambda x: x.replace('\n', ' '))


def apply_lemmatization(df):
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    wl = WordNetLemmatizer()
    nr = len(df)
    lis = []
    for r in range(0, nr):
        ll = []
        t = df.loc[r]['Resume']
        tw = str(t).split(" ")
        for w in tw:
            ll.append(wl.lemmatize(w, pos="v"))
        lt = " ".join(ll)
        lis.append(lt)
    df['Resume'] = lis


def remove_stop_words(df):
    nltk.download('stopwords')
    sw = list(stopwords.words('english'))
    for s in sw:
        rs = r"\b" + s + r"\b"
        df['Resume'] = df['Resume'].str.replace(rs, '')


def encode_labels(df):
    encoder = LabelEncoder()
    df['Category'] = encoder.fit_transform(df['Category'])
    return encoder.classes_



def main():
    connection = connect_database()
    df = download_dataset(connection, "dataset_raw")
    convert_to_lower_case(df)
    remove_short_words(df)
    remove_punctuations(df)
    apply_lemmatization(df)
    classes = encode_labels(df)
    df_train, df_test = train_test_split(df, test_size=0.3, random_state=42, stratify=df["Category"])
    save_dataset(df_train, connection, "dataset_train")
    save_dataset(df_test, connection, "dataset_test")
    save_classes(classes, connection)
    connection.close()


if __name__ == "__main__":
    main()
