__author__ = 'Kristian'

from MyUtil.csvFileFixer import csvFileFixer
import csv
import matplotlib.pyplot as plt
import numpy as np
import sys


class graphPlotter():

    delimiter = ""

    def __init__(self, delimiter):
        """ Init method """
        self.delimiter = delimiter

    def plot(self, fromCsvFile, col1, col1Name, col2, col2Name):
        """ Plots out the csvFile. Takes 2 columns and their names. """
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
    #fileName = 'csvFiles/DA_EXCEL_FOR_DA_PRICE_FORECAST'
    #fileName1 = 'csvFiles/STATION_LIST_AVERAGE_COMBINING'
    #filePath = fileName + '.csv'
    #document = fileName + '_FIXED.csv'
    #cleanedDocument = fileName + '_CLEANED.csv'
    #twoRows = fileName + '_2ROWS.csv'
    #correctedData = fileName + '_CORRECTED_DATA.csv'

    fileName = 'csvFiles/PRICE_CONSUMPTION_WEATHER_COMBI'
    filePath = fileName + '.csv'
    #document = fileName + '_FIXED.csv'
    cleanedDocument = fileName + '_CLEANED.csv'
    twoRows = fileName + '_2ROWS.csv'
    correctedData = fileName + '_CORRECTED_DATA.csv'

    fileFixer = csvFileFixer(",")
    #fileFixer.fixDateFormat(filePath, document, 0)

    #Price vs Temperature
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2, 4])
    fileFixer.printCsvDocument(cleanedDocument)
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 2, 4)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [0])
    gp = graphPlotter(",")
    gp.plot(correctedData, 1, "Price", 0, "Temperature")

    #Price vs Wind speed
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [3, 2])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 3, 4)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [1])
    gp2 = graphPlotter(",")
    gp2.plot(correctedData, 0, "Wind speed", 1, "Price")

    #Price vs Consumption
    #fileFixer.fixDateFormat(filePath1, document1, 0)
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2, 5])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 2, 5)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [0])
    gp1 = graphPlotter(",")
    gp1.plot(correctedData, 0, "Price", 1, "Consumption")

    #Temperature vs Consumption
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [4, 5])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 4, 5)
    #fileFixer.removeToHighAndToLow(twoRows, correctedData, [0])
    gp2 = graphPlotter(",")
    gp2.plot(twoRows, 0, "Temperature", 1, "Consumption")

    #Wind speed vs Consumption
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [3, 5])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 3, 5)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [1])
    gp2 = graphPlotter(",")
    gp2.plot(correctedData, 0, "Wind speed", 1, "Consumption")

    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2])
    fileFixer.concatenateWeekdaysAndGiveAverages(cleanedDocument, 6, 2)
if __name__ == '__main__':
    main()