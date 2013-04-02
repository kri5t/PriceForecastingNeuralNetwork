__author__ = 'Kristian'

from MyUtil.csvFileFixer import csvFileFixer
import csv
import matplotlib.pyplot as plt
import numpy as np


class graphPlotter():

    def __init__(self):
        """ Init method """

    def plot(self, fromCsvFile, col1, col2):
        plt.plotfile(fromCsvFile, delimiter=';', cols=(col1, col2),
                     names=('Wind Speed', 'Electricity Price'), linestyle='None', marker='.')

        y = []
        x = []

        with open(fromCsvFile, 'rb') as csvFile:
            dat = csv.reader(csvFile, delimiter=';')
            for row in dat:
                y.append(int(row[col2]))
                x.append(int(row[col1]))

        m, b = np.polyfit(x, y, 1)
        plt.plot(x, np.array(x) * m + b, color='red')

        plt.show()


def main():
    document = '/Users/kristian/Downloads/CSV_FORMAT_PRICES_FIXED.csv'

    fileFixer = csvFileFixer()
    fileFixer.printCsvDocument(document)

    gp = graphPlotter()
    gp.plot(document, 0, 1)

if __name__ == '__main__':
    main()