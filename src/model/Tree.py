from Model import Model
from sklearn import tree


class Tree(Model):

    def __init__(self, params, filepath=None):
        super().__init__(params, filepath)

    def _init_model(self, params):
        return tree.DecisionTreeClassifier()
