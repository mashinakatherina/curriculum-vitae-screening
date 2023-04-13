from sklearn.neighbors import KNeighborsClassifier

from Model import Model


class KNN(Model):

    def __init__(self, params, filepath=None):
        super().__init__(params, filepath)

    def _init_model(self, params):
        return KNeighborsClassifier(n_neighbors=7)
