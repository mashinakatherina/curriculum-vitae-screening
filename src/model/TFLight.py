from Model import Model
import tensorflow as tf
import numpy as np


# inference only
class TFLight(Model):

    def __init__(self, params, filepath=None):
        super().__init__(params, filepath)

    def _load_model(self, filename):
        interpreter = tf.lite.Interpreter(filename, num_threads=20)
        interpreter.allocate_tensors()
        return interpreter

    def fit(self, x, y):
        pass

    def predict(self, x):
        pred = []
        input_index = self._model.get_input_details()[0]["index"]
        output_index = self._model.get_output_details()[0]["index"]
        for i in range(x.shape[0]):
            self._model.set_tensor(input_index, np.array([x[i]], dtype=np.float32))
            self._model.invoke()
            pred.append(self._model.get_tensor(output_index))
        return np.array(pred).reshape((x.shape[0], pred[0].shape[1]))

    def save(self, filename):
        pass
