import os.path
import sys
import shutil

from keras.utils import to_categorical

from util.database import download_dataset, connect_database, upload_model, check_model
from src.tokenization import tokenize_dataset

from model_names import models


def main(model_name):
    with open("../version.txt", "r") as version_file:
        version = int(version_file.readline()) + 1
    if model_name not in models.keys():
        raise Exception("Model with name " + model_name + " is not found")
    connection = connect_database()
    model_id = check_model(connection, model_name, version)
    if model_id is not None:
        raise Exception("Model with name " + model_name + " and version " + str(version) + " is already exists in "
                                                                                           "database")
    if not os.path.isdir("./saved"):
        os.mkdir("saved")
    df = download_dataset(connection, "dataset_train", int_categories=True)
    x_train, y_train = tokenize_dataset(df)
    params = {}
    filename = "model" + models[model_name][2]
    if models[model_name][1] == "tensorflow":
        y_train = to_categorical(y_train, num_classes=25, dtype='float32')
        params["input_length"] = x_train.shape[1]
    model = models[model_name][0](params)
    model.fit(x_train, y_train)
    model.save(os.path.join("saved", filename))
    shutil.make_archive("model", "zip", "saved")

    upload_model(connection, model_name, "model.zip", version)
    connection.close()


if __name__ == "__main__":
    main(sys.argv[1])
