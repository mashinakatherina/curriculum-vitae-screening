import os.path
import sys
import shutil
import time

import numpy as np

from util.database import download_dataset, connect_database, upload_metrics, download_model, check_model
from tokenization import tokenize_dataset

from sklearn.metrics import accuracy_score

from model_names import models


def calculate_accuracy(pred, gt):
    return accuracy_score(gt, pred)


def main(model_name):
    with open("../version.txt", "r") as version_file:
        version = int(version_file.readline()) + 1
    if model_name not in models.keys():
        raise Exception("Model with name " + model_name + " is not found")
    connection = connect_database()
    model_id = check_model(connection, model_name, version)
    if model_id is None:
        raise Exception("Model with name " + model_name + " and version " + str(version) + " is not exists in "
                                                                                           "database")
    df = download_dataset(connection, "dataset_test", int_categories=True)
    x_test, y_test = tokenize_dataset(df)

    download_model(connection, model_name, "loaded.zip", version)
    os.makedirs("loaded")
    shutil.unpack_archive("loaded.zip", "loaded", "zip")
    params = {}
    filename = "model" + models[model_name][2]
    if models[model_name][1] == "tensorflow":
        params["input_length"] = x_test.shape[1]
    model = models[model_name][0](params, os.path.join(".", "loaded", filename))
    start = time.time()
    preds = model.predict(x_test)
    end = time.time()
    duration = end - start
    if models[model_name][1] == "tensorflow":
        preds = np.array([np.argmax(i) for i in preds])
    accuracy = calculate_accuracy(preds, y_test)

    upload_metrics(connection, accuracy, duration, model_id)

    connection.close()


if __name__ == "__main__":
    main(sys.argv[1])
