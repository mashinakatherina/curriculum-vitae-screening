import pickle


class Model:

    def __init__(self, params, filename=None):
        self._model = self._init_model(params) if not filename else self._load_model(filename)

    def _load_model(self, filename):
        with open(filename, "rb") as file:
            return pickle.load(file)

    def _init_model(self, params):
        return None

    def fit(self, x, y):
        self._model.fit(x, y)

    def predict(self, x):
        return self._model.predict(x)

    def save(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self._model, file)
