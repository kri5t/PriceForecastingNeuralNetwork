import sys
import csv
from pybrain.datasets import SupervisedDataSet

DS = SupervisedDataSet(3, 2)
DS.appendLinked([1, 2, 3], [4, 5])
sys.stdout.write("hello\n")
sys.stdout.write(DS['input'])

class GreenEnergyDataSet(SupervisedDataSet):
    """ A dataset for the XOR function."""
    def __init__(self):
        SupervisedDataSet.__init__(self, 2, 1)

        with open('C:\Users\Brian\Desktop\Brian\Universitetet\Kandidat\Master Thesis\WeLoveGREEN-ENERGY\DATASET_FOR_GREEN_ENERGY_PLOTTING\wind_temp_production.csv', 'rb') as csvfile:
            dat = csv.reader(csvfile, delimiter=';')
            for row in dat:
            #  print 'sample 0: ' + row[0] + ' sample 1: ' + row[1]
                self.addSample([int(row[1]),int(row[2])],[int(row[0])])