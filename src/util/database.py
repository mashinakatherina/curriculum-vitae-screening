import os
import psycopg2
import pandas as pd
from psycopg2 import sql


def connect_database():
    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    conn = psycopg2.connect(
        host="vgorash.ddns.net",
        database="ai_architecture",
        user=username,
        password=password)
    return conn


def save_dataset(df, connection, table_name, create_indices=False):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("DROP TABLE IF EXISTS {table}").format(table=sql.Identifier(table_name)))
    if create_indices:
        cursor.execute(sql.SQL("CREATE TABLE {table}(id int primary key, resume text, category text)")
                       .format(table=sql.Identifier(table_name)))
    else:
        cursor.execute(sql.SQL("CREATE TABLE {table}(id int primary key, resume text, category int)")
                       .format(table=sql.Identifier(table_name)))
    for index, row in df.iterrows():
        cursor.execute(sql.SQL("INSERT INTO {table}(id, resume, category) values (%s, %s, %s)")
                       .format(table=sql.Identifier(table_name)),
                       (index if create_indices else row["Id"], row["Resume"], row["Category"]))
    cursor.close()
    connection.commit()


def save_classes(classes, connection):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("DROP TABLE IF EXISTS classes"))
    cursor.execute(sql.SQL("CREATE TABLE classes(id int primary key, label text)"))
    for i in range(len(classes)):
        cursor.execute(sql.SQL("INSERT INTO classes(id, label) values (%s, %s)"), (i, classes[i]))
    cursor.close()
    connection.commit()

def download_dataset(connection, table_name, int_categories=False):
    cursor = connection.cursor()
    cursor.execute(sql.SQL("SELECT * FROM {table}").format(table=sql.Identifier(table_name)))
    result = cursor.fetchall()
    resumes = []
    categories = []
    ids = []
    for row in result:
        ids.append(row[0])
        resumes.append(row[1])
        categories.append(int(row[2]) if int_categories else row[2])
    df = pd.DataFrame({"Id": ids, "Resume": resumes, "Category": categories})
    cursor.close()
    return df
