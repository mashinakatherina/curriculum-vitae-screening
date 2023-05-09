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


def upload_model(connection, model_name, filename, version):
    cursor = connection.cursor()
    with open(filename, "rb") as file:
        cursor.execute("INSERT INTO models (version, model_name, data) VALUES (%s, %s, %s)",
                       (str(version), model_name, file.read()))
    cursor.close()
    connection.commit()


def check_model(connection, model_name, version):
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM models WHERE version = %s and model_name = %s", (str(version), model_name))

    if cursor.fetchone()[0] > 0:
        cursor.execute("SELECT id FROM models WHERE version = %s and model_name = %s", (str(version), model_name))
        value = cursor.fetchone()[0]
        cursor.close()
        return value
    cursor.close()
    return None


def download_model(connection, model_name, filename, version):
    model_id = check_model(connection, model_name, version)
    if model_id is None:
        raise Exception("Model " + model_name + " with version " + str(version) + " is not presented in table")
    download_model_by_id(connection, model_id, filename)


def get_model_info_by_id(connection, model_id):
    cursor = connection.cursor()
    cursor.execute("SELECT model_name, version FROM models WHERE id = %s", (str(model_id),))
    value = cursor.fetchone()
    cursor.close()
    return value


def download_model_by_id(connection, model_id, filename):
    cursor = connection.cursor()
    cursor.execute("SELECT data FROM models WHERE id = %s", (str(model_id),))
    model = cursor.fetchone()[0]
    with open(filename, "wb") as file:
        file.write(model)
    cursor.close()


def upload_metrics(connection, accuracy, duration, model_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO metrics (accuracy, duration, model_id) VALUES (%s, %s, %s)",
                   (str(accuracy), str(duration), str(model_id)))
    cursor.close()
    connection.commit()


def get_metrics(connection, version):
    cursor = connection.cursor()
    cursor.execute("SELECT count(*)"
                   " FROM metrics inner join models m on m.id = metrics.model_id where version = %s", str(version))
    if cursor.fetchone()[0] > 0:
        cursor.execute("SELECT id, accuracy, duration"
                       " FROM metrics inner join models m on m.id = metrics.model_id where version = %s", str(version))
        values = cursor.fetchall()
        cursor.close()
        return values
    cursor.close()
    return None


def get_deployment(connection, version):
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM deployments where version = %s", str(version))
    if cursor.fetchone()[0] > 0:
        cursor.execute("SELECT model_id, score FROM deployments where version = %s", str(version))
        value = cursor.fetchone()
        cursor.close()
        return value
    cursor.close()
    return None


def add_deployment(connection, version, deployment):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO deployments (version, model_id, score) VALUES (%s, %s, %s)",
                   (version, str(deployment[0]), str(deployment[1])))
    cursor.close()
    connection.commit()


def get_category_name(connection, category):
    cursor = connection.cursor()
    cursor.execute("SELECT label from classes where id = %s", (str(category),))
    value = cursor.fetchone()
    cursor.close()
    return value[0]
