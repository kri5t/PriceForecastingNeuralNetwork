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
                    maximum = 99
                    lowest = 1
                    maxPercentile.append(np.percentile(temporary, maximum))
                    print "MaxPercentile: " + str(np.percentile(temporary, maximum))
                    minPercentile.append(np.percentile(temporary, lowest))
                    print "MinPercentile: " + str(np.percentile(temporary, lowest))
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

    def normalizeZeroToOneUsingCSV(self, inputDocument, outputDocument, rowNumber, temperatureRow, hourRow, weekdaysRow
                                   , dateRow, useSeasonal, useHourlyMatrix, useWeekdaysMatrix, useSeasonMatrix,
                                   usePaperPrices, priceRow):
        """
        Returns an array that contains a normalization of the 4 input types:
        consumption, wind speed, temperature, price

        Temperature is converted to kelvin to always get a positive number.
        """
        useLastDaysPrice = True
        useWeekdaysRow = True
        useDateRow = True
        firstOutput = False
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
                        if not rowNumber[index] == hourRow and not rowNumber[index] == weekdaysRow and not rowNumber[
                            index] == dateRow:
                            temporaryArray.append(float(row[rowNumber[index]]))
                            if rowNumber[index] == priceRow:
                                value = row[rowNumber[index]]
                                priceDict.update({line: value})
                                line += 1
                        else:
                            temporaryArray.append(row[rowNumber[index]])
                    arrayOfData.append(temporaryArray)
                    #for something in priceDict:
                    #print priceDict[something]
                for index in range(len(arrayOfData)):
                    if not rowNumber[index] == hourRow and not rowNumber[index] == weekdaysRow and not rowNumber[
                        index] == dateRow:
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
                            add = 24
                            if row > (28 * 24):
                                if usePaperPrices:
                                    rowToWrite.append(
                                        self.normalizeValue(float(priceDict[row - (7 * add)]), maxVal, minVal))
                                    rowToWrite.append(
                                        self.normalizeValue(float(priceDict[row - (7 * add)]), maxVal, minVal))
                                    rowToWrite.append(
                                        self.normalizeValue(float(priceDict[row - (7 * add)]), maxVal, minVal))
                                    rowToWrite.append(
                                        self.normalizeValue(float(priceDict[row - (14 * add)]), maxVal, minVal))
                                    rowToWrite.append(
                                        self.normalizeValue(float(priceDict[row - (21 * add)]), maxVal, minVal))
                                    rowToWrite.append(
                                        self.normalizeValue(float(priceDict[row - (28 * add)]), maxVal, minVal))
                                    rowToWrite.append(
                                        self.normalizeValue(float(priceDict[row - (1 * add)]), maxVal, minVal))
                                    rowToWrite.append(
                                        self.normalizeValue(float(priceDict[row - (1 * add)]), maxVal, minVal))
                                    rowToWrite.append(
                                        self.normalizeValue(float(priceDict[row - (1 * add)]), maxVal, minVal))
                                if add == 24:
                                    rowToWrite.append(self.normalizeValue(float(priceDict[row - 1]), maxVal, minVal))
                            else:
                                for i in range(0, 9, 1):
                                    rowToWrite.append(0)

                                    #rowToWrite.append(self.lastPrice)

                        if rowNumber[column] == hourRow:
                            #print self.normalizeHourToArray(arrayOfData[column][row])
                            if useHourlyMatrix:
                                for hour in self.normalizeHourToArray(arrayOfData[column][row]):
                                    rowToWrite.append(float(hour))
                            else:
                                for hour in self.normalizeHour(arrayOfData[column][row]):
                                    rowToWrite.append(hour)
                                    #print hour
                        elif rowNumber[column] == weekdaysRow and useWeekdaysRow:
                            if useWeekdaysMatrix:
                                for day in self.normalizeDaysToArray(arrayOfData[column][row]):
                                    rowToWrite.append(float(day))
                            else:
                                for day in self.normalizeDays(arrayOfData[column][row]):
                                    rowToWrite.append(day)
                        elif rowNumber[column] == dateRow and useDateRow:
                            if useSeasonal:
                                if useSeasonMatrix:
                                    for date in self.normalizeDateToArray(arrayOfData[column][row]):
                                        rowToWrite.append(float(date))
                                else:
                                    for date in self.normalizeDate(arrayOfData[column][row]):
                                        rowToWrite.append(date)
                            else:
                                if useSeasonMatrix:
                                    for date in self.normalizeDateToMonthArray(arrayOfData[column][row]):
                                        rowToWrite.append(float(date))
                                else:
                                    for date in self.normalizeDateToMonth(arrayOfData[column][row]):
                                        rowToWrite.append(date)

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
                    if row > (28 * 24):
                        if not firstOutput:
                            print rowToWrite
                            firstOutput = True
                        writer.writerow(rowToWrite)

    def normalizeValue(self, val, maxVal, minVal):
        val = float(val)
        maxVal = float(maxVal)
        minVal = float(minVal)
        return (val - ((maxVal + minVal) / 2.0)) / ((maxVal - minVal) / 2.0)
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

    def normalizeDays(self, day):
        value = {'Mon': 0,
                 'Tue': 1,
                 'Wed': 2,
                 'Thu': 3,
                 'Fri': 4,
                 'Sat': 5,
                 'Sun': 6}.get(day, 0)
        return [float(value - float(6.0 / 2.0)) / float(6.0 / 2.0)]

    def normalizeDaysToArray(self, day):
        value = {'Mon': [1, 0, 0, 0, 0, 0, 0],
                 'Tue': [0, 1, 0, 0, 0, 0, 0],
                 'Wed': [0, 0, 1, 0, 0, 0, 0],
                 'Thu': [0, 0, 0, 1, 0, 0, 0],
                 'Fri': [0, 0, 0, 0, 1, 0, 0],
                 'Sat': [0, 0, 0, 0, 0, 1, 0],
                 'Sun': [0, 0, 0, 0, 0, 0, 1]}.get(day, [0, 0, 0, 0, 0, 0, 0])
        return value

    def normalizeDate(self, date):
        month = int(date.split("/")[0])
        value = 0
        if month == 12 or month == 1 or month == 2:
            value = 0
        if month == 3 or month == 4 or month == 5:
            value = 1
        if month == 6 or month == 7 or month == 8:
            value = 2
        if month == 9 or month == 10 or month == 11:
            value = 3
        return [float(value - float(3.0 / 2.0)) / float(3.0 / 2.0)]

    def normalizeDateToArray(self, date):
        month = int(date.split("/")[0])
        if month == 12 or month == 1 or month == 2:
            return [1, 0, 0, 0]
        if month == 3 or month == 4 or month == 5:
            return [0, 1, 0, 0]
        if month == 6 or month == 7 or month == 8:
            return [0, 0, 1, 0]
        if month == 9 or month == 10 or month == 11:
            return [0, 0, 0, 1]

    def normalizeDateToMonth(self, date):
        month = int(date.split("/")[0])
        value = {1: 0,
                 2: 1,
                 3: 2,
                 4: 3,
                 5: 4,
                 6: 5,
                 7: 6,
                 8: 7,
                 9: 8,
                 10: 9,
                 11: 10,
                 12: 11}.get(month, 0)
        return [float(value - float(11.0 / 2.0)) / float(11.0 / 2.0)]

    def normalizeDateToMonthArray(self, date):
        month = int(date.split("/")[0])
        value = {1: [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 2: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 3: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 4: [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 5: [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                 6: [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                 7: [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                 8: [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                 9: [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                 10: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 11: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                 12: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}.get(month, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        return value


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
    dateRow = 0

    useHourlyMatrix = True
    useWeekdaysMatrix = True
    useSeasonMatrix = False
    useSeasons = False
    usePaperPrices = True

    fileName = '../csvFiles/YEAR_2011_2012_DA_EXCEL_FOR_DA_PRICE_FORECAST_06-05-2013'
    filePath = fileName + '.csv'
    toKelvin = fileName + '_kelvin.csv'
    cleanedDocument = fileName + '_CLEANED.csv'
    correctedData = fileName + '_CORRECTED_DATA.csv'
    zeroToOneFile = ("/Users/kristian/git/TheNetwork/EncogNeuralNetwork/runFilesFolder/"
                     + "PAPERPrice_Consumption_windSpeed_timeOfDayMATRIX_weekdaysMATRIX_1pTrim.csv")

    #fixer.printCsvDocument(filePath)

    fixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument, [consumptionRow, windSpeedRow, priceRow])
    fixer.removeUsingPercentile(cleanedDocument, correctedData, [priceRow])
    fixer.fahrenheitToKelvin(correctedData, toKelvin, temperatureRow)
    fixer.normalizeZeroToOneUsingCSV(toKelvin, zeroToOneFile,
                                     [consumptionRow, windSpeedRow, timeOfDayRow, weekdaysRow, priceRow],
                                     temperatureRow, timeOfDayRow, weekdaysRow, dateRow,  useSeasons,
                                     useHourlyMatrix, useWeekdaysMatrix, useSeasonMatrix, usePaperPrices,
                                     priceRow)

    if False:
        preFix = ""
        useHourlyMatrix = False
        useWeekdaysMatrix = False
        useSeasonMatrix = False
        useSeasons = False
        usePaperPrices = False
        listOfFiles = [
            "MATRIX_Price_Consump_windSpeed_temperatureRow_timeOfDay_weekdays_seasonOfYear",
            "MIXEDPrice_Consump_windSpeed_temperatureRow_timeOfDayMATRIX_weekdays_seasonOfYearMATRIX",
            "MIXEDPrice_Consump_windSpeed_temperatureRow_timeOfDayMATRIX_monthOfYearMATRIX_PREDICT1371560863501",
            "MATRIX_Price_Consump_windSpeed_timeOfDay_weekdays_monthOfYear_PREDICT1371470595375",
            "MIXEDPrice_Consump_windSpeed_temperatureRow_timeOfDayMATRIX_weekdays",
            "MIXEDPrice_Consump_windSpeed_temperatureRow_timeOfDayMATRIX_seasonOfYearMATRIX",
            "MIXEDPrice_Consump_windSpeed_temperatureRow_timeOfDayMATRIX_weekdays_monthOfYearMATRIX",
            "MIXEDPrice_Consump_windSpeed_temperatureRow_timeOfDay_weekdays_seasonOfYearMATRIX",
            "MIXEDPrice_Consump_windSpeed_temperatureRow_timeOfDay_weekdaysMATRIX_monthOfYearMATRIX",
            "MIXEDPrice_Consump_windSpeed_timeOfDayMATRIX_weekdays_monthOfYearMATRIX"]
        for i in range(2):
            for file in listOfFiles:
                myArray = []
                if "MATRIX" in file[:6]:
                    useHourlyMatrix = True
                    useWeekdaysMatrix = True
                    useSeasonMatrix = True
                if i == 1:
                    usePaperPrices = True
                    file = "PAPER" + file
                if "Consump" in file:
                    myArray += [consumptionRow]
                if "windSpeed" in file:
                    myArray += [windSpeedRow]
                if "temperatureRow" in file:
                    myArray += [temperatureRow]
                if "timeOfDay" in file:
                    if "timeOfDayMATRIX" in file:
                        myArray += [timeOfDayRow]
                        useHourlyMatrix = True
                    else:
                        myArray += [timeOfDayRow]
                if "weekdays" in file:
                    if "weekdaysMATRIX" in file:
                        myArray += [weekdaysRow]
                        useWeekdaysMatrix = True
                    else:
                        myArray += [weekdaysRow]
                if "monthOfYear" in file:
                    if "monthOfYearMATRIX" in file:
                        myArray += [dateRow]
                        useSeasonMatrix = True
                    else:
                        myArray += [dateRow]
                if "seasonOfYear" in file:
                    if "seasonOfYearMATRIX" in file:
                        myArray += [dateRow]
                        useSeasonMatrix = True
                        useSeasons = True
                    else:
                        myArray += [dateRow]
                        useSeasons = True
                if "Price" in file:
                    myArray += [priceRow]

                zeroToOneFile = ("/Users/kristian/git/TheNetwork/EncogNeuralNetwork"
                                 + "/runFilesFolder/" + file + ".csv")
                fixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument,
                                                     [consumptionRow, windSpeedRow, priceRow])
                fixer.removeUsingPercentile(cleanedDocument, correctedData, [priceRow])
                fixer.fahrenheitToKelvin(correctedData, toKelvin, temperatureRow)
                fixer.normalizeZeroToOneUsingCSV(toKelvin, zeroToOneFile,
                                                 myArray,
                                                 temperatureRow, timeOfDayRow, weekdaysRow, dateRow, useSeasons,
                                                 useHourlyMatrix, useWeekdaysMatrix, useSeasonMatrix, usePaperPrices,
                                                 priceRow)
    elif False:
        useMatrix = False
        useSeasons = False
        usePaperPrices = False
        for j in range(2):
            fileParameters = ""
            if j is 0:
                fileParameters += "runFilesFolder/MIXED00Price_Consump_"
            for i in range(1, 3):
                otherParameters = fileParameters
                myStartArray = []
                if i == 0:
                    myStartArray += []
                    otherParameters += ""
                if i == 1:
                    myStartArray += [windSpeedRow]
                    otherParameters += "windSpeed_"
                if i == 2:
                    myStartArray += [windSpeedRow, temperatureRow]
                    otherParameters += "windSpeed_temperatureRow_"
                if i == 3:
                    myStartArray += [temperatureRow]
                    otherParameters += "temperatureRow_"

                for k in range(1, 8):
                    lastParameters = otherParameters
                    myArray = [consumptionRow]
                    myArray += myStartArray
                    useHourlyMatrix = True
                    useWeekdaysMatrix = True
                    useSeasonMatrix = False
                    print myArray
                    if k is 0:
                        myArray += [timeOfDayRow]
                        lastParameters += "timeOfDay"
                        useSeasons = False
                    if k is 1:
                        myArray += [timeOfDayRow, dateRow]
                        lastParameters += "timeOfDayMATRIX_monthOfYearMATRIX"
                        useSeasons = False
                    if k is 2:
                        myArray += [timeOfDayRow, dateRow]
                        lastParameters += "timeOfDayMATRIX_seasonOfYearMATRIX"
                        useSeasons = True
                    if k is 3:
                        myArray += [timeOfDayRow, weekdaysRow]
                        lastParameters += "timeOfDayMATRIX_weekdays"
                        useSeasons = False
                    if k is 4:
                        myArray += [timeOfDayRow, weekdaysRow, dateRow]
                        lastParameters += "timeOfDayMATRIX_weekdays_monthOfYear"
                        useSeasons = False
                    if k is 5:
                        myArray += [timeOfDayRow, weekdaysRow, dateRow]
                        lastParameters += "timeOfDayMATRIX_weekdays_seasonOfYear"
                        useSeasons = True
                    if k is 6:
                        myArray += [weekdaysRow]
                        lastParameters += "weekdays"
                        useSeasons = False
                    if k is 7:
                        myArray += [weekdaysRow, dateRow]
                        lastParameters += "weekdays_monthOfYearMATRIX"
                        useSeasons = False
                    if k is 8:
                        myArray += [weekdaysRow, dateRow]
                        lastParameters += "weekdays_seasonOfYearMATRIX"
                        useSeasons = True
                    if k is 9:
                        myArray += [dateRow]
                        lastParameters += "monthOfYear"
                        useSeasons = False
                    if k is 10:
                        myArray += [dateRow]
                        lastParameters += "seasonOfYear"
                        useSeasons = True
                    if k is 11:
                        myArray += []
                        lastParameters += ""
                        useSeasons = False
                    myArray += [priceRow]
                    zeroToOneFile = ("/Users/kristian/git/TheNetwork/EncogNeuralNetwork"
                                     + "/" + lastParameters + "00.csv")
                    fixer.cleanMinusAndNullInDocumentRow(filePath, cleanedDocument,
                                                         [consumptionRow, windSpeedRow, priceRow])
                    #fixer.removeUsingPercentile(cleanedDocument, correctedData, [priceRow])
                    fixer.fahrenheitToKelvin(cleanedDocument, toKelvin, temperatureRow)
                    fixer.normalizeZeroToOneUsingCSV(toKelvin, zeroToOneFile,
                                                     myArray,
                                                     temperatureRow, timeOfDayRow, weekdaysRow, dateRow, useSeasons,
                                                     useHourlyMatrix, useWeekdaysMatrix, useSeasonMatrix,
                                                     usePaperPrices, priceRow)
    else:
        print "LOL"

if __name__ == '__main__':
    main()