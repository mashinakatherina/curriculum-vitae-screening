import os
import shutil
import tensorflow as tf
from model.NN import NN
from util.database import connect_database, check_model, download_model, upload_model


def main():
    with open("../version.txt", "r") as version_file:
        version = int(version_file.readline()) + 1
    connection = connect_database()
    model_id = check_model(connection, "nn", version)
    if model_id is None:
        raise Exception("Model with name 'nn' and version " + str(version) + " is not exists in database")
    download_model(connection, "nn", "loaded.zip", version)
    os.makedirs("loaded")
    shutil.unpack_archive("loaded.zip", "loaded", "zip")
    params = {"input_length": 2500}
    filename = "model.h5"
    model = NN(params, os.path.join(".", "loaded", filename))
    converter = tf.lite.TFLiteConverter.from_keras_model(model._model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_quant_model = converter.convert()
    if not os.path.isdir("saved"):
        os.mkdir("saved")
    with open(os.path.join("saved", "model.bin"), "wb") as f:
        f.write(tflite_quant_model)
    shutil.make_archive("model", "zip", "saved")
    upload_model(connection, "tflight", "model.zip", version)
    connection.close()


if __name__ == "__main__":
    main()
