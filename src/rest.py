import shutil

import numpy as np
from flask import Flask, request
import pandas as pd
import os

from model_names import models
from util.database import connect_database, get_deployment, download_model_by_id, get_model_info_by_id, \
    get_category_name
from dataset_processing import preprocess_dataset
from tokenization import tokenize_dataset, load_tokenizer


def clean_downloads():
    if os.path.isdir("loaded"):
        shutil.rmtree("loaded")
    if os.path.isdir("tokenizer_loaded"):
        shutil.rmtree("tokenizer_loaded")


clean_downloads()
tokenizer = load_tokenizer()
connection = connect_database()


def prepare_data(resume):
    df = pd.DataFrame({"Resume": [resume], "Category": [0]})
    print(df)
    preprocess_dataset(df)
    return tokenize_dataset(df, tokenizer)[0]


def prepare_model(version):
    model_id = get_deployment(connection, version)[0]
    model_name = get_model_info_by_id(connection, model_id)[0]
    download_model_by_id(connection, model_id, "loaded.zip")
    os.makedirs("loaded")
    shutil.unpack_archive("loaded.zip", "loaded", "zip")
    params = {}
    filename = "model" + models[model_name][2]
    if models[model_name][1] == "tensorflow":
        params["input_length"] = 2500
    model = models[model_name][0](params, os.path.join(".", "loaded", filename))
    return model, model_name


with open("../version.txt", "r") as version_file:
    version = int(version_file.readline())
loaded_model, m_name = prepare_model(version)
app = Flask(__name__)


@app.route('/api/resume', methods=['POST'])
def process_resume():
    inp = prepare_data(request.data.decode("utf-8"))
    preds = loaded_model.predict(inp)
    if models[m_name][1] == "tensorflow":
        preds = np.array([np.argmax(i) for i in preds])
    return get_category_name(connection, preds[0])


@app.route('/admin/loadModel/<model_version>', methods=['POST'])
def update_model(model_version):
    global loaded_model, m_name
    clean_downloads()
    loaded_model, m_name = prepare_model(model_version)
    print("Updated to version " + str(model_version))
    return "Updated to version " + str(model_version)


if __name__ == '__main__':
    app.run(host='192.168.0.174', port=8080)
