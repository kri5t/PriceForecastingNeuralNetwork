import collections
import csv
import sys
import os
import sqlite3
import numpy as np

from datetime import datetime


class csvFileFixer():
    delimiter = ''
    c = None
    lastPrice = 0

    def __init__(self, delimiter, useDB):
        """ Init method """
        self.delimiter = delimiter
        if useDB:
            conn = sqlite3.connect('csvFiles/database.db')
            self.c = conn.cursor()

    def fixDateFormat(self, filePath, fileToSaveToPath, rowNumberToFix):
        """Hand a file to it and it fixes the format"""
        with open(fileToSaveToPath, 'wb') as writeFile:
            with open(filePath, 'rU') as csvFile:
                reader = csv.reader(csvFile, delimiter=self.delimiter)
                writer = csv.writer(writeFile, delimiter=self.delimiter)
                for row in reader:

                    if len(row[rowNumberToFix]) > 8:
                        row[rowNumberToFix] = str(row[rowNumberToFix])[3:5] + "/" + str(row[0])[0:2] + "/" + str(
                            row[0])[8:10]
                        if str(row[0])[0:1] == "0": row[rowNumberToFix] = str(row[rowNumberToFix])[1:]
                    writer.writerow(row)

    def copyRow(self, fromDocument, rowToCopy, toDocument, toWhatRow):
        """Copy one row from one document to another document"""
        with open(toDocument, 'wb') as writeFile:
            with open(fromDocument, 'rU') as readFile:
                reader = csv.reader(readFile, delimiter=self.delimiter)
                writer = csv.writer(writeFile, delimiter=self.delimiter)
                for row in reader:
                    sys.stdout.write(str(len(row)))

    def printCsvDocument(self, documentToPrint):
        """Prints the specified CSV document"""
        with open(documentToPrint, 'rU') as readFile:
            reader = csv.reader(readFile, delimiter=self.delimiter)
            indexPrinted = False
            for row in reader:
                if indexPrinted is False:
                    sys.stdout.write("Number of rows in csvFile: " + str(len(row)) + "\n")
                    indexPrinted = True

                for index in range(len(row)):
                    sys.stdout.write(row[index] + "\t\t")
                sys.stdout.write("\n")

    def cleanMinusAndNullInDocumentRow(self, document, toDocument, columns):
        """Removes minus signs and Null values"""
        flag = True
        written = 0
        rowsBeforeCleaning = 0
        with open(toDocument, 'wb') as writeToFile:
            with open(document, 'rU') as readFromFile:
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)
                skipFirstRow = False
                for row in reader:
                    if skipFirstRow is False:
                        for r in columns:
                            castToInt = str(row[r]).replace(",", ".").replace(" ", "")
                            if "-" in castToInt or castToInt is "" or int(round(float(castToInt))) == 0:
                                flag = False
                            else:
                                row[r] = int(round(float(castToInt)))
                        if flag:
                            writer.writerow(row)
                            written += 1
                            flag = True
                        else:
                            flag = True
                    else:
                        skipFirstRow = False
                    rowsBeforeCleaning += 1
        print "Rows cleaned: " + str(rowsBeforeCleaning - written)

    def removeToHighAndToLow(self, document, toDocument, columns):
        """

        """
        value = [len(columns)]
        numberOfValues = [len(columns)]
        medians = [len(columns)]
        entries = 0
        entriesWritten = 0
        with open(toDocument, 'wb') as writeToFile:
            with open(document, 'rU') as readFromFile:

                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)
                for row in reader:
                    entries += 1
                    for index in range(len(columns)):
                        if value[index] is None:
                            value[index] = int(row[columns[index]])
                        else:
                            value[index] += int(round(float(row[columns[index]])))
                        numberOfValues[index] += 1
                for index in range(len(value)):
                    medians[index] = value[index] / numberOfValues[index]
                readFromFile.seek(0)
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                for row in reader:
                    for index in range(len(columns)):
                        if int(medians[index] + medians[index]) > int(round(float(row[columns[index]]))) > 0:
                            writer.writerow(row)
                            entriesWritten += 1
        sys.stdout.write(str(entries - entriesWritten) + "\n")

    def removeUsingPercentile(self, document, toDocument, columns):
        """
        """
        maxPercentile = []
        #print maxPercentile
        minPercentile = []
        entries = 0
        entriesWritten = 0
        with open(toDocument, 'wb') as writeToFile:
            with open(document, 'rU') as readFromFile:
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)
                for index in range(len(columns)):
                    temporary = []
                    for row in reader:
                        temporary.append(float(row[columns[index]]))
                        #print temporary
                    maxPercentile.append(np.percentile(temporary, 99))
                    print np.percentile(temporary, 99)
                    minPercentile.append(np.percentile(temporary, 1))
                    print np.percentile(temporary, 1)
                readFromFile.seek(0)
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                for row in reader:
                    entries += 1
                    for index in range(len(columns)):
                        #print "max: " + str(maxPercentile) + " mid: " + str(
                        #    int(round(float(row[columns[index]])))) + "min: " + str(minPercentile)
                        if maxPercentile[0] > int(round(float(row[columns[index]]))) > minPercentile[0]:
                            writer.writerow(row)
                            entriesWritten += 1
        sys.stdout.write("Percentile removal: " + str(entries - entriesWritten) + "\n")

    def twoRowsToOneFile(self, document, toFile, row1, row2):
        """
        Creates new CSV file with only 2 rows
        """
        with open(toFile, 'wb') as writeToFile:
            with open(document, 'rU') as readFromFile:
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)
                for row in reader:
                    writer.writerow([row[row1], row[row2]])

    def concatenateEntriesAndGiveAverage(self, document, casesRow, priceRow, arrayOfCases):
        """
        Concatenates the prices for the given cases and creates an array of average price.
        :param document: document to read from
        :param casesRow: What row to read cases from
        :param priceRow: The row to get prices from
        :param arrayOfCases: An array of what cases to concatenate
        :return:
        """
        numberOfWeekdays = [0] * len(arrayOfCases)
        weekdaysCombined = [0] * len(arrayOfCases)
        medianPricesForAllWeekdays = [0] * len(arrayOfCases)
        with open(document, 'rU') as readFromFile:
            reader = csv.reader(readFromFile, delimiter=self.delimiter)
            for row in reader:
                for index in range(len(arrayOfCases)):
                    if row[casesRow] == arrayOfCases[index]:
                        numberOfWeekdays[index] += 1
                        weekdaysCombined[index] += float(row[priceRow])
        for index in range(len(numberOfWeekdays)):
            medianPricesForAllWeekdays[index] = weekdaysCombined[index] / numberOfWeekdays[index]
            #sys.stdout.write("median: " + str(medianPricesForAllWeekdays[index]) + "  sumOfPrice: " + str(
            #weekdaysCombined[index]) + "  numberOfTimes: " + str(numberOfWeekdays[index]) + "\n")
        #sys.stdout.write("\n")
        return medianPricesForAllWeekdays

    def priceFluctuationOnSameHours(self, document, rowsToMeasureOn, priceRow, toDocument):
        """
        """
        lowMargin = [0] * len(rowsToMeasureOn)
        highMargin = [0] * len(rowsToMeasureOn)
        highestPrice = 0
        lowestPrice = 0
        prices = []
        dato = None

        with open(toDocument, 'wb') as writeToFile:
            with open(document, 'rU') as readFromFile:
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)
                initialized = False
                theSame = True
                for row in reader:
                    if not initialized:
                        for index in range(len(rowsToMeasureOn)):
                            lowMargin[index] = float(row[rowsToMeasureOn[index]]) - float(
                                row[rowsToMeasureOn[index]]) / 50
                            highMargin[index] = float(row[rowsToMeasureOn[index]]) + float(
                                row[rowsToMeasureOn[index]]) / 50
                        initialized = True
                        dato = row[0]
                    else:
                        for index in range(len(rowsToMeasureOn)):
                            if lowMargin[index] < float(row[rowsToMeasureOn[index]]) < highMargin[index]:
                                theSame = True
                            else:
                                theSame = False
                        if theSame:
                            prices.append(row[priceRow])
                        else:
                            writer.writerow(row)

                        theSame = True
                    for index in range(len(prices)):
                        if float(prices[index]) < 80:
                            prices.pop(index)

        for price in prices:
            if highestPrice is 0 and lowestPrice is 0:
                highestPrice = price
                lowestPrice = price
            else:
                if int(round(float(price))) < lowestPrice:
                    lowestPrice = int(round(float(price)))
                elif highestPrice < int(round(float(price))):
                    highestPrice = int(round(float(price)))
        pricesDistribution = []
        intervalPrice = lowestPrice
        while float(intervalPrice) < float(highestPrice):
            pricesDistribution.append(intervalPrice)
            intervalPrice += 10
        numberOfPricesSeen = [0] * len(pricesDistribution)
        for price in prices:
            for index in range(len(pricesDistribution)):
                if float(pricesDistribution[index]) < float(price) < float(pricesDistribution[index] + 10):
                    numberOfPricesSeen[index] += 1
        seen = len(prices)
        print(highMargin)
        print(lowMargin)
        return [numberOfPricesSeen, pricesDistribution, seen, lowestPrice, highestPrice, dato]

    def priceDistributionOnAllSimilarDays(self, document, rowsToMeasureOn, priceRow, toDocument):
        """

        """
        timesSeenAndHiAndLow = []
        stop = False
        swap = True
        while not stop:
            if swap:
                values = self.priceFluctuationOnSameHours(document, rowsToMeasureOn, priceRow, toDocument)
                swap = False
            else:
                values = self.priceFluctuationOnSameHours(toDocument, rowsToMeasureOn, priceRow, document)
                swap = True
            if values[2] > 20:
                #timesSeenAndHiAndLowObject = [values[2], int(values[4]), int(values[4]), values[3], values[3]]
                timesSeenAndHiAndLowObject = [datetime.strptime(values[5], "%m/%d/%y"), int(values[4]), int(values[4]),
                                              int(values[3]), int(values[3])]
                #print(timesSeenAndHiAndLowObject)
                timesSeenAndHiAndLow.append(timesSeenAndHiAndLowObject)
            if os.stat(document).st_size < 20:
                stop = True
        print(timesSeenAndHiAndLow)
        return timesSeenAndHiAndLow

    def fahrenheitToCelsius(self, document, toFile, rowNumber):
        """
        Converts fahrenheit to celsius in the given row.
        Takes a csv-file to read from and writes to a new file.
        """
        with open(toFile, 'wb') as writeToFile:
            with open(document, 'rU') as readFromFile:
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)
                skipFirstRow = True
                for row in reader:
                    if not skipFirstRow and row[rowNumber] != "-":
                        row[rowNumber] = int(round((float(row[rowNumber]) - 32.0) * 5.0 / 9.0))
                        writer.writerow(row)
                    else:
                        skipFirstRow = False

    def fahrenheitToKelvin(self, document, toFile, rowNumber):
        """
        Converts fahrenheit to celsius in the given row.
        Takes a csv-file to read from and writes to a new file.
        """
        with open(toFile, 'wb') as writeToFile:
            with open(document, 'rU') as readFromFile:
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)
                skipFirstRow = True
                for row in reader:
                    if not skipFirstRow and row[rowNumber] != "-":
                        #print row[rowNumber]
                        #print ((float(row[rowNumber]) - 32.0) * (5.0 / 9.0)) + 273.0
                        row[rowNumber] = ((float(row[rowNumber]) - 32.0) * (5.0 / 9.0)) + 273.0
                        writer.writerow(row)
                    else:
                        skipFirstRow = False

    def normalizeZeroToOne(self, inputDocument, outputDocument, rowNumber):
        """
        Returns an array that contains a normalization of the 4 input types:
        consumption, wind speed, temperature, price

        Temperature is converted to kelvin to always get a positive number.
        """
        tableName = "startMajData"
        rowsToNormalize = ("consumption", "windSpeed", "temperature", "price")
        arrayOfNormalizedValues = []
        print len(arrayOfNormalizedValues)
        for index in range(len(rowsToNormalize)):
            if rowsToNormalize[index] == "temperature":
                constant = 273.15
            else:
                constant = 0
            maxValue = int(
                self.c.execute("SELECT MAX(" + rowsToNormalize[index] + ") FROM " + tableName).fetchone()[0]) + constant
            minValue = int(
                self.c.execute("SELECT MIN(" + rowsToNormalize[index] + ") FROM " + tableName).fetchone()[0]) + constant
            array = []
            print rowsToNormalize[index] + " maxValue: " + str(maxValue)
            print rowsToNormalize[index] + " minValue: " + str(minValue)
            for row in self.c.execute("SELECT " + rowsToNormalize[index] + " FROM " + tableName):
                normalizedValue = (
                    float(float(row[0] + constant) - float(minValue)) / float(float(maxValue) - float(minValue)))
                array.append(normalizedValue)
            arrayOfNormalizedValues.append(array)
        print arrayOfNormalizedValues
        print len(arrayOfNormalizedValues)
        return arrayOfNormalizedValues
        #self.c.execute("DROP TABLE dataKristianNormalized")

    def normalizeZeroToOneUsingCSV(self, inputDocument, outputDocument, rowNumber, temperatureRow, hourRow
                                   , useLastDaysPrice, priceRow):
        """
        Returns an array that contains a normalization of the 4 input types:
        consumption, wind speed, temperature, price

        Temperature is converted to kelvin to always get a positive number.
        """
        arrayOfData = []
        arrayOfMax = []
        arrayOfMin = []
        arrayOfNormalizedValues = []
        priceDict = collections.OrderedDict()
        print "LENGTH: " + str(len(rowNumber))
        print len(arrayOfNormalizedValues)
        with open(outputDocument, 'wb') as writeToFile:
            with open(inputDocument, 'rU') as readFromFile:
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)

                for index in range(len(rowNumber)):
                    temporaryArray = []
                    readFromFile.seek(0)
                    line = 0
                    for row in reader:
                        if not rowNumber[index] == hourRow:
                            temporaryArray.append(float(row[rowNumber[index]]))
                            if rowNumber[index] == priceRow:
                                value = row[rowNumber[index]]
                                #print "val " + value
                                #priceDict['line'] = value
                                priceDict.update({line: value})
                                line += 1
                        else:
                            temporaryArray.append(row[rowNumber[index]])
                    arrayOfData.append(temporaryArray)
                for something in priceDict:
                    print priceDict[something]
                for index in range(len(arrayOfData)):
                    if not rowNumber[index] == hourRow: #and not rowNumber[index] == priceRow:
                        if rowNumber[index] == temperatureRow:
                            constant = 273.15
                        else:
                            constant = 0
                        arrayOfMax.append(max(arrayOfData[index]) + constant)
                        arrayOfMin.append(min(arrayOfData[index]) + constant)
                    #elif rowNumber[index] == priceRow:
                    #    arrayOfMax.append(1560.99)
                    #    arrayOfMin.append(-14.84)
                    else:
                        arrayOfMax.append(0)
                        arrayOfMin.append(0)
                        #print arrayOfMin
                    #print arrayOfMax
                print arrayOfMax
                print arrayOfMin
                for row in range(len(arrayOfData[0])):
                    rowToWrite = []
                    for column in range(len(arrayOfData)):
                        maxVal = float(arrayOfMax[column])
                        minVal = float(arrayOfMin[column])
                        if rowNumber[column] == temperatureRow:
                            constant = 273.15
                            #print arrayOfData[column][row]
                        else:
                            constant = 0.0

                        if rowNumber[column] == priceRow and useLastDaysPrice:
                            if self.lastPrice == 0:
                                self.lastPrice = self.normalizeValue(float(arrayOfData[column][row]), maxVal, minVal)
                            rowToWrite.append(self.lastPrice)

                        if rowNumber[column] == hourRow:
                            #print self.normalizeHourToArray(arrayOfData[column][row])
                            for hour in self.normalizeHourToArray(arrayOfData[column][row]):
                                rowToWrite.append(hour)
                                #print hour
                        else:
                            val = float(arrayOfData[column][row] + constant)
                            #0 to 1:
                            #normalizedValue = ((val - minVal) / (maxVal - minVal))
                            #-1 to 1:
                            normalizedValue = self.normalizeValue(val, maxVal, minVal)
                            if rowNumber[column] == priceRow:
                                self.lastPrice = normalizedValue
                            rowToWrite.append(normalizedValue)
                            #print rowToWrite

                    writer.writerow(rowToWrite)

    def normalizeValue(self, val, maxVal, minVal):
        return (val - ((maxVal + minVal) / 2)) / ((maxVal - minVal) / 2)
        #return val

    def normalizeHour(self, hour):
        value = {'00-01': 0,
                 '01-02': 1,
                 '02-03': 2,
                 '03-04': 3,
                 '04-05': 4,
                 '05-06': 5,
                 '06-07': 6,
                 '07-08': 7,
                 '08-09': 8,
                 '09-10': 9,
                 '10-11': 10,
                 '11-12': 11,
                 '12-13': 12,
                 '13-14': 13,
                 '14-15': 14,
                 '15-16': 15,
                 '16-17': 16,
                 '17-18': 17,
                 '18-19': 18,
                 '19-20': 19,
                 '20-21': 20,
                 '21-22': 21,
                 '22-23': 22,
                 '23-00': 23}.get(hour, 0)
        #return float(float(value) / 23.0)
        return [float(value - float(23.0 / 2.0)) / float(23.0 / 2.0)]

    def normalizeHourToArray(self, hour):
        value = {'00-01': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '01-02': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '02-03': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '03-04': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '04-05': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '05-06': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '06-07': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '07-08': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '08-09': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '09-10': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '10-11': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '11-12': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '12-13': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '13-14': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '14-15': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 '15-16': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 '16-17': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 '17-18': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 '18-19': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 '19-20': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                 '20-21': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 '21-22': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 '22-23': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 '23-00': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        }.get(hour, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        return value
        #return float(float(value) / 23.0)
        #return float(value - float(23.0 / 2.0)) / float(23.0 / 2.0)


def main():
    fixer = csvFileFixer(",", False)

    priceRow = 5
    consumptionRow = 2
    temperatureRow = 4
    windSpeedRow = 3
    weekdaysRow = 10
    timeOfDayRow = 1
    windDirection = 8
    windProduction = 6
    pressure = 7

    fileName = '../csvFiles/YEAR_2011_2012_DA_EXCEL_FOR_DA_PRICE_FORECAST_06-05-2013'
    filePath = fileName + '.csv'
    toKelvin = fileName + '_kelvin.csv'
    cleanedDocument = fileName + '_CLEANED.csv'
    correctedData = fileName + '_CORRECTED_DATA.csv'
    zeroToOneFile = ("/Users/kristian/Documents/workspace/EncogNeuralNetwork"
                     + "/YEAR_2012_DA_EXCEL_FOR_DA_PRICE_FORECAST_29-04-2013_ZeroToOne.csv")
    brian = ("/Users/kristian/Documents/workspace/EncogNeuralNetwork"
             + "/YEAR_2012_DA_EXCEL_FOR_DA_PRICE_FORECAST_29-04-2013_Brian.csv")

    #fixer.printCsvDocument(filePath)

    fixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [consumptionRow, windSpeedRow, priceRow])
    fixer.removeUsingPercentile(cleanedDocument, correctedData, [priceRow])
    fixer.fahrenheitToKelvin(correctedData, toKelvin, temperatureRow)
    fixer.normalizeZeroToOneUsingCSV(toKelvin, zeroToOneFile,
                                     [consumptionRow, windSpeedRow, timeOfDayRow, priceRow],
                                     temperatureRow, timeOfDayRow, True, priceRow)

    #fixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [consumptionRow, windSpeedRow, priceRow, pressure])
    #fixer.fahrenheitToKelvin(cleanedDocument, toKelvin, temperatureRow)
    #fixer.removeUsingPercentile(toKelvin, correctedData, [windProduction])
    #fixer.normalizeZeroToOneUsingCSV(correctedData, brian,
    #                                 [consumptionRow, windSpeedRow, timeOfDayRow, temperatureRow, pressure,
    #                                  windProduction], temperatureRow, timeOfDayRow, False, priceRow)


if __name__ == '__main__':
    main()