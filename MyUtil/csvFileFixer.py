import csv
import sys
import os


class csvFileFixer():
    delimiter = ''

    def __init__(self, delimiter):
        """ Init method """
        self.delimiter = delimiter

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
        with open(toDocument, 'wb') as writeToFile:
            with open(document, 'rU') as readFromFile:
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)
                skipFirstRow = True
                for row in reader:
                    if skipFirstRow is False:
                        for r in columns:
                            castToInt = str(row[r]).replace(",", ".").replace(" ", "")
                            if "-" in castToInt or castToInt is "":
                                flag = False
                            else:
                                row[r] = int(round(float(castToInt)))
                        if flag:
                            writer.writerow(row)
                            flag = True
                        else:
                            flag = True

                    else:
                        skipFirstRow = False

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
                            value[index] += int(row[columns[index]])
                        numberOfValues[index] += 1
                for index in range(len(value)):
                    medians[index] = value[index] / numberOfValues[index]
                readFromFile.seek(0)
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                for row in reader:
                    for index in range(len(columns)):
                        if int(medians[index] + medians[index]) > int(row[columns[index]]) > 0:
                            writer.writerow(row)
                            entriesWritten += 1
        sys.stdout.write(str(entries - entriesWritten) + "\n")

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
            sys.stdout.write("median: " + str(medianPricesForAllWeekdays[index]) + "  sumOfPrice: " + str(
                weekdaysCombined[index]) + "  numberOfTimes: " + str(numberOfWeekdays[index]) + "\n")
        sys.stdout.write("\n")
        return medianPricesForAllWeekdays

    def priceFluctuationOnSameHours(self, document, rowsToMeasureOn, priceRow, toDocument):
        """
        """
        lowMargin = [0] * len(rowsToMeasureOn)
        highMargin = [0] * len(rowsToMeasureOn)
        highestPrice = 0
        lowestPrice = 0
        prices = []

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
                        #print(lowMargin)
                        #print(highMargin)
                        initialized = True
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
        #print(pricesDistribution)
        #print(numberOfPricesSeen)
        #print(len(prices))
        seen = len(prices)
        return [numberOfPricesSeen, pricesDistribution, seen, lowestPrice, highestPrice]

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
                timesSeenAndHiAndLowObject = [values[2], values[4], values[3]]
                print(timesSeenAndHiAndLowObject)
                timesSeenAndHiAndLow.append(timesSeenAndHiAndLowObject)
            if os.stat(document).st_size < 20:
                stop = True

    def fahrenheitToCelsius(self, document, toFile, rowNumber):
        with open(toFile, 'wb') as writeToFile:
            with open(document, 'rU') as readFromFile:
                reader = csv.reader(readFromFile, delimiter=self.delimiter)
                writer = csv.writer(writeToFile, delimiter=self.delimiter)
                skipFirstRow = True
                for row in reader:
                    if not skipFirstRow and row[rowNumber] != "-":
                        sys.stdout.write(row[rowNumber])
                        sys.stdout.write(str((int(row[rowNumber]) - 32) * 5 / 9))
                        row[rowNumber] = ((int(row[rowNumber]) - 32) * 5 / 9)
                        writer.writerow(row)
                    else:
                        skipFirstRow = False


def main():
    fixer = csvFileFixer(",")
    filePath = 'DA_EXCEL_FOR_DA_PRICE_FORECAST.csv'
    fileToSaveToPath = 'DA_EXCEL_FOR_DA_PRICE_FORECAST_FIXED.csv'

    fixer.fixDateFormat(filePath, fileToSaveToPath, 0)
    fixer.printCsvDocument('DA_EXCEL_FOR_DA_PRICE_FORECAST_FIXED.csv')


if __name__ == '__main__':
    main()