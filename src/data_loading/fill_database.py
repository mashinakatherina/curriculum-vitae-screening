import pandas as pd
import sys
import psycopg2
from progress.bar import Bar


def connect_database():
    conn = psycopg2.connect(
        host="vgorash.ddns.net",
        database="ai_architecture",
        user="github",
        password="password")
    return conn


def process_csv(filename):
    df = pd.read_csv(filename)
    connection = connect_database()
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS dataset")
    cursor.execute("CREATE TABLE dataset(id int primary key, resume text, category text)")
    print("Uploading data to database")
    bar = Bar("Upload progress", max=len(df))
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO dataset(id, resume, category) values (%s, %s, %s)",
                       (index, row["Resume"], row["Category"]))
        bar.next()
    bar.finish()
    cursor.close()
    print("Committing changes")
    connection.commit()
    connection.close()
    print("Data uploaded")


if __name__ == "__main__":
    process_csv(sys.argv[1])
