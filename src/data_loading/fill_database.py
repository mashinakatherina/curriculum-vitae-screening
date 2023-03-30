import os
import pandas as pd
import sys
import psycopg2
from progress.bar import Bar


def connect_database():
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    conn = psycopg2.connect(
        host="vgorash.ddns.net",
        database="ai_architecture",
        user=username,
        password=password)
    return conn


def process_csv(filename):
    df = pd.read_csv(filename)
    print("Connecting to database")
    connection = connect_database()
    cursor = connection.cursor()
    print("Cleaning old table")
    cursor.execute("DROP TABLE IF EXISTS dataset")
    print("Creating new table")
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
