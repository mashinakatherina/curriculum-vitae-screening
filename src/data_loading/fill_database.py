import pandas as pd
import sys
import psycopg2


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
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO dataset(id, resume, category) values (%s, %s, %s)",
                       (index, row["Resume"], row["Category"]))
    cursor.close()
    connection.commit()
    connection.close()


if __name__ == "__main__":
    process_csv(sys.argv[1])
