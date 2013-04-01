import sys
from pybrain.datasets import SupervisedDataSet

DS = SupervisedDataSet(3, 2)
DS.appendLinked([1, 2, 3], [4, 5])
sys.stdout.write("hello\n")
sys.stdout.write(DS['input'])

sys.stdout.closed