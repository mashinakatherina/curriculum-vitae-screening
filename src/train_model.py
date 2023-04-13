import os.path
import sys
import shutil

from keras.utils import to_categorical

from model.Tree import Tree
from model.KNN import KNN
from model.NN import NN
from util.database import download_dataset, connect_database, upload_model, download_model, check_model
from util.tokenization import tokenize_dataset

models = {"tree": (Tree, "sklearn"), "knn": (KNN, "sklearn"), "nn": (NN, "tensorflow")}


def main(model_name):
    with open("../version.txt", "r") as version_file:
        version = int(version_file.readline()) + 1
    if model_name not in models.keys():
        raise Exception("Model with name " + model_name + " is not found")
    connection = connect_database()
    if check_model(connection, model_name, version):
        raise Exception("Model with name " + model_name + " and version " + str(version) + " is already exists in "
                                                                                           "database")
    if not os.path.isdir("./saved"):
        os.mkdir("saved")
    df = download_dataset(connection, "dataset_train", int_categories=True)
    x_train, y_train = tokenize_dataset(df)
    params = {}
    filename = "model.sav" if models[model_name][1] == "sklearn" else "model.h5"
    if models[model_name][1] == "tensorflow":
        y_train = to_categorical(y_train, num_classes=25, dtype='float32')
        params["input_length"] = x_train.shape[1]
    model = models[model_name][0](params)
    model.fit(x_train, y_train)
    model.save(os.path.join("saved", filename))
    shutil.make_archive("model", "zip", "saved")

    upload_model(connection, model_name, "model.zip", 1)
    connection.close()


if __name__ == "__main__":
    main(sys.argv[1])
