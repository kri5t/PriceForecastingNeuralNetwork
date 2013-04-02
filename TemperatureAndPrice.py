__author__ = 'Kristian'

from MyUtil.csvFileFixer import csvFileFixer
import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

class graphPlotter():

    delimiter = ""

    def __init__(self, delimiter):
        """ Init method """
        self.delimiter = delimiter

    def plot(self, fromCsvFile, col1, col1Name, col2, col2Name):
        #myData = mlab.csv2rec(fromCsvFile, delimiter=';', skiprows=1)
        #myData.dump('/Users/kristian/Downloads/DUMP.csv')
        plt.plotfile(fromCsvFile, delimiter=self.delimiter, cols=(col1, col2), skiprows=1,
                     names=(col1Name, col2Name), linestyle='None', marker='.')

        y = []
        x = []

        with open(fromCsvFile, 'rb') as csvFile:
            dat = csv.reader(csvFile, delimiter=self.delimiter)
            for row in dat:
                y.append(int(row[col2]))
                x.append(int(row[col1]))

        m, b = np.polyfit(x, y, 1)
        plt.plot(x, np.array(x) * m + b, color='red')

        plt.show()


def main():
    fileName = 'DA_EXCEL_FOR_DA_PRICE_FORECAST'
    filePath = fileName + '.csv'
    #document = fileName + '_FIXED.csv'
    cleanedDocument = fileName + '_CLEANED.csv'
    twoRows = fileName + '_2ROWS.csv'
    correctedData = fileName + '_CORRECTED_DATA.csv'

    fileFixer = csvFileFixer(",")
    #fileFixer.fixDateFormat(filePath, document, 0)
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2, 4])
    fileFixer.printCsvDocument(cleanedDocument)
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 2, 4)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [0])
    gp = graphPlotter(",")
    gp.plot(correctedData, 1, "DK1", 0, "Temperature")

if __name__ == '__main__':
    main()