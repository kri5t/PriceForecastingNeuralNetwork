from matplotlib.finance import candlestick
from MyUtil.csvFileFixer import csvFileFixer
import csv
import matplotlib.pyplot as plt
import numpy as np
from time import time

__author__ = 'Kristian'


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

    ax.bar(ind, arrayOfDays, width, color='b')

    # add some
    ax.set_ylabel('Average price')
    ax.set_title('Average price over all days')
    ax.set_xticks(ind + (width * 2))
    ax.set_xticklabels(weekdays)


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


def barPlotPrices(arrayOfTimes, tickLabels):
    """

    :param arrayOfTimes:
    """
    N = len(arrayOfTimes)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.25       # the width of the bars

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(ind, arrayOfTimes, width, color='b')

    # add some
    ax.set_ylabel('Number of times seen')
    ax.set_title('Same hour price distribution')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(tickLabels)


def candleStickGraph(inputData):
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.2)
    ax = fig.add_subplot(111)
    ax.set_xticklabels()
    ax.set_title()
    #ax.xaxis.set_minor_formatter(dayFormatter)

    #plot_day_summary(ax, quotes, ticksize=3)
    candlestick(ax, inputData, width=0.2)

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    #plt.show()


def main():
    fileName = 'csvFiles/YEAR_2011_2012_DA_EXCEL_FOR_DA_PRICE_FORECAST_06-05-2013'
    originalFile = fileName + '.csv'
    filePath = fileName + 'CELSIUS.csv'
    #document = fileName + '_FIXED.csv'
    cleanedDocument = fileName + '_CLEANED.csv'
    twoRows = fileName + '_2ROWS.csv'
    correctedData = fileName + '_CORRECTED_DATA.csv'
    swapFile = fileName + '_SWAP_FILE.csv'

    fileFixer = csvFileFixer(",", False)
    gp = graphPlotter(",")
    #fileFixer.fixDateFormat(filePath, document, 0)
    startTime = time()
    fileFixer.fahrenheitToCelsius(originalFile, filePath, 4)

    #Price vs Temperature
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 2, 4)
    fileFixer.removeUsingPercentile(twoRows, correctedData, [0])
    gp.plot(correctedData, 1, "Price", 0, "Temperature")

    #Print the document:
    fileFixer.printCsvDocument(cleanedDocument)

    #Price vs Wind speed
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [3, 2])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 3, 2)
    fileFixer.removeUsingPercentile(twoRows, correctedData, [1])
    gp.plot(correctedData, 0, "Wind speed", 1, "Price")

    #Price vs Consumption
    #fileFixer.fixDateFormat(filePath1, document1, 0)
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2, 5])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 2, 5)
    fileFixer.removeUsingPercentile(twoRows, correctedData, [0])
    gp.plot(correctedData, 0, "Price", 1, "Consumption")

    #Temperature vs Consumption
    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [5])
    fileFixer.twoRowsToOneFile(cleanedDocument, twoRows, 4, 5)
    #fileFixer.removeToHighAndToLow(twoRows, correctedData, [1])
    gp.plot(twoRows, 0, "Temperature", 1, "Consumption")

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

    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2, 3, 5])
    #labelAndValues = fileFixer.priceFluctuationOnSameHours(cleanedDocument, [3, 4, 5], 2, swapFile)
    #barPlotPrices(labelAndValues[0], labelAndValues[1])

    fileFixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [2, 3, 5])
    fileFixer.priceDistributionOnAllSimilarDays(cleanedDocument, [3, 4, 5], 2, swapFile)
    #barPlotPrices(labelAndValues[0], labelAndValues[1])
    print("TIME: " + str(time() - startTime))

    plt.show()


if __name__ == '__main__':
    main()