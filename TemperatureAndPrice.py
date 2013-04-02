__author__ = 'Kristian'

from MyUtil.csvFileFixer import csvFileFixer
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

class graphPlotter():

    def __init__(self):
        """ Init method """

    def plot(self, fromCsvFile, col1, col1Name, col2, col2Name):
        #myData = mlab.csv2rec(fromCsvFile, delimiter=';', skiprows=1)
        #myData.dump('/Users/kristian/Downloads/DUMP.csv')
        plt.plotfile(fromCsvFile, delimiter=';', cols=(col1, col2), skiprows=1,
                     names=(col1Name, col2Name), linestyle='None', marker='.')

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
    cleanedDocument = '/Users/kristian/Downloads/CSV_FORMAT_PRICES_CLEANED.csv'
    twoRows = '/Users/kristian/Downloads/CSV_FORMAT_PRICES_2rows.csv'
    correctedData = '/Users/kristian/Downloads/CSV_FORMAT_PRICES_correctedData.csv'

    fileFixer = csvFileFixer()
    fileFixer.cleanMinusAndNullInDocumentRow(document, cleanedDocument, [2, 4])
    fileFixer.printCsvDocument(cleanedDocument)
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 2, 4)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [0])
    gp = graphPlotter()
    gp.plot(correctedData, 1, "DK1", 0, "Temperature")

if __name__ == '__main__':
    main()