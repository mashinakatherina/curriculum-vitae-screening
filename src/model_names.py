from model.Tree import Tree
from model.KNN import KNN
from model.NN import NN
from model.TFLight import TFLight

models = {"tree": (Tree, "sklearn", ".sav"),
          "knn": (KNN, "sklearn", ".sav"),
          "nn": (NN, "tensorflow", ".h5"),
          "tflight": (TFLight, "tensorflow", ".bin")}
