from sklearn.feature_extraction.text import CountVectorizer


def tokenize_dataset(df):
    cv = CountVectorizer(max_features=2500)
    x = cv.fit_transform(df['Resume']).toarray()
    y = df['Category']
    return x, y
