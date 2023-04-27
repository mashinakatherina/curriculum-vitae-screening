from keras import Sequential, models
from keras.layers import Embedding, Conv1D, MaxPool1D, Dropout, GlobalMaxPooling1D, Dense

from Model import Model


class NN(Model):

    def __init__(self, params, filepath=None):
        super().__init__(params, filepath)

    def _init_model(self, params):
        model = Sequential()
        model.add(Embedding(input_dim=232337, output_dim=100, input_length=params["input_length"]))
        model.add(Conv1D(128, 3, activation='relu'))
        model.add(MaxPool1D(3))
        model.add(Dropout(0.3))
        model.add(Conv1D(128, 3, activation='relu'))
        model.add(GlobalMaxPooling1D())
        model.add(Dropout(0.3))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(32, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(25, activation='softmax'))

        model.compile(loss='binary_crossentropy', optimizer="adam", metrics=['accuracy'])

        return model

    def fit(self, x, y):
        self._model.fit(x, y, batch_size=64, epochs=20, verbose=1)

    def save(self, filename):
        self._model.save(filename)

    def _load_model(self, filename):
        return models.load_model(filename)
