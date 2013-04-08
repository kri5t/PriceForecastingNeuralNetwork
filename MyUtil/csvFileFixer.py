import csv
import sys


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

    def priceFluctuationOnAverageDay(self):
        """

        """


def main():
    fixer = csvFileFixer()
    filePath = 'DA_EXCEL_FOR_DA_PRICE_FORECAST.csv'
    fileToSaveToPath = 'DA_EXCEL_FOR_DA_PRICE_FORECAST_FIXED.csv'

    fixer.fixDateFormat(filePath, fileToSaveToPath, 0)
    fixer.printCsvDocument('DA_EXCEL_FOR_DA_PRICE_FORECAST_FIXED.csv')


if __name__ == '__main__':
    main()