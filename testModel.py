
from model.model import Model

myModel=Model()
myModel.buildGraph(2010, 2016)
n,e=myModel.getGraphDetails()
print(f"Numero di nodi: ", n)
print(f"Numero di archi: ", e)