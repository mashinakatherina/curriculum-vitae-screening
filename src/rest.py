import shutil

import numpy as np
from flask import Flask, request
import pandas as pd
import os

from model_names import models
from util.database import connect_database, get_deployment, download_model_by_id, get_model_info_by_id
from dataset_processing import preprocess_dataset
from src.tokenization import tokenize_dataset


def do_the_screening(data):
    print(prepare_data(data))
    return prepare_data(data)


def prepare_data(resume):
    df = pd.DataFrame({"Resume": [resume], "Category": [0]})
    print(df)
    preprocess_dataset(df)
    return tokenize_dataset(df)[0]

def prepare_model(version):
    connection = connect_database()
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


loaded_model, m_name = prepare_model(3)
app = Flask(__name__)


@app.route('/neural_network', methods=['POST'])
def process_resume():
    inp = prepare_data(request.data.decode("utf-8"))
    preds = loaded_model.predict(inp)
    if models[m_name][1] == "tensorflow":
        preds = np.array([np.argmax(i) for i in preds])
    return str(preds[0])


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80)
