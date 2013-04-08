__author__ = 'Kristian'

from MyUtil.csvFileFixer import csvFileFixer
import csv
import matplotlib.pyplot as plt
import numpy as np


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

        #plt.show()


def barPlotWeekdays(arrayOfDays, weekdays):
    """

    :param arrayOfDays:
    """
    N = 7
    ind = np.arange(N)  # the x locations for the groups
    width = 0.25       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)

    reacts1 = ax.bar(ind, arrayOfDays, width, color='b')

    # add some
    ax.set_ylabel('Average price')
    ax.set_title('Average price over all days')
    ax.set_xticks(ind + (width * 2))
    ax.set_xticklabels(weekdays)

    #ax.legend(reacts1[0])

    #plt.show()


def barPlotTime(arrayOfTimes):
    """

    :param arrayOfTimes:
    """
    N = 24
    ind = np.arange(N)  # the x locations for the groups
    width = 0.25       # the width of the bars

    month = ["00", "01", "02", "03", "04", "05", "06", "07", "08",
             "09", "10", "11", "12", "13", "14", "15", "16", "17",
             "18", "19", "20", "21", "22", "23"]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(ind, arrayOfTimes, width, color='b')

    # add some
    ax.set_ylabel('Average price')
    ax.set_title('Hourly average price')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(month)

    #ax.legend(reacts1[0])

    #plt.show()


def main():
    fileName = 'csvFiles/PRICE_CONSUMPTION_WEATHER_COMBI'
    filePath = fileName + '.csv'
    #document = fileName + '_FIXED.csv'
    cleanedDocument = fileName + '_CLEANED.csv'
    twoRows = fileName + '_2ROWS.csv'
    correctedData = fileName + '_CORRECTED_DATA.csv'

    fileFixer = csvFileFixer(",")
    gp = graphPlotter(",")
    #fileFixer.fixDateFormat(filePath, document, 0)

    #Price vs Temperature
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2, 4])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 2, 4)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [0])
    gp.plot(correctedData, 1, "Price", 0, "Temperature")

    #Print the document:
    fileFixer.printCsvDocument(cleanedDocument)

    #Price vs Wind speed
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [3, 2])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 3, 4)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [1])
    gp.plot(correctedData, 0, "Wind speed", 1, "Price")

    #Price vs Consumption
    #fileFixer.fixDateFormat(filePath1, document1, 0)
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2, 5])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 2, 5)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [0])
    gp.plot(correctedData, 0, "Price", 1, "Consumption")

    #Temperature vs Consumption
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [4, 5])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 4, 5)
    fileFixer.removeToHighAndToLow(twoRows, correctedData, [0])
    gp.plot(correctedData, 0, "Temperature", 1, "Consumption")

    #Wind speed vs Consumption
    #fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [3, 5])
    #fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 3, 5)
    #fileFixer.removeToHighAndToLow(twoRows, correctedData, [1])
    #gp.plot(correctedData, 0, "Wind speed", 1, "Consumption")

    #Average price for each day.
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2])
    barPlotWeekdays(fileFixer.concatenateEntriesAndGiveAverage(cleanedDocument, 6, 2, weekdays), weekdays)

    #Average price for each hour per day
    timesOfDay = ["00-01", "01-02", "02-03", "03-04", "04-05", "05-06", "06-07", "07-08", "08-09",
                  "09-10", "10-11", "11-12", "12-13", "13-14", "14-15", "15-16", "16-17", "17-18",
                  "18-19", "19-20", "20-21", "21-22", "22-23", "23-00"]
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2])
    barPlotTime(fileFixer.concatenateEntriesAndGiveAverage(cleanedDocument, 1, 2, timesOfDay))

    plt.show()


if __name__ == '__main__':
    main()