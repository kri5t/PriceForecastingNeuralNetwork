import csv
import multiprocessing
from os import listdir
from os.path import isfile, join
import threading
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from multiprocessing import JoinableQueue as Queue, Process as Thread
from datetime import datetime
import sys
import time


class Plotter():
    pdfName = ""
    fileName = ""
    dbg = multiprocessing.get_logger().info

    def __init__(self, fileName, pdfName):
        """ Init method """
        self.pdfName = pdfName
        self.fileName = fileName

    def printIdealActualOutput(self, pathName):
        actualProduction = []
        idealProduction = []
        lengthArray = []

        bestMae = 99999
        bestMpe = 99999

        bestMaeFileName = ""
        bestMpeFileName = ""

        onlyFiles = [f for f in listdir(pathName) if isfile(join(pathName, f))]

        for fileName in onlyFiles:
            if "PREDIC" not in fileName: continue
            name = pathName + fileName
            print "fileName: ", name

            mae = 0
            mpe = 0

            with open(name, 'rb') as csvfile:
                dat = csv.reader(csvfile, delimiter=',')
                headers = dat.next()

                i = 0
                for row in dat:
                    if not "TOTAL" in row[0]:

                        tempMae = (int(float(row[0].replace(',', '.'))) - int(float(row[1].replace(',', '.'))))
                        mae += float(abs(tempMae))

                        tempMpe = float((abs(tempMae) * 100) / int(float(row[1].replace(',', '.'))))
                        mpe += tempMpe

                        # if tempMpe>50:
                        #print "Psycho MPE = " , tempMpe , " with actual: " , row[0].replace(',','.') , " and ideal: " , row[1].replace(',','.')
                        if tempMae > 200:
                            print "Psycho MAE = ", tempMae, " with actual: ", row[0].replace(',', '.'), " and ideal: ",
                            row[
                                1].replace(',', '.')

                        actualProduction.append(int(float(row[0].replace(',', '.'))))
                        idealProduction.append(int(float(row[1].replace(',', '.'))))
                        i += 1
                        lengthArray.append(i)

                mpe = mpe / i
                mae = mae / i

                if mpe < bestMpe:
                    bestMpe = mpe
                    bestMpeFileName = name

                if mae < bestMae:
                    bestMae = mae
                    bestMaeFileName = name

                print "MAE : ", mae
                print "MPE : ", mpe

        print ""
        print "BEST MAE : ", bestMae
        print "In file: ", bestMaeFileName, "\n"
        print "BEST MPE : ", bestMpe
        print "In file: ", bestMpeFileName

    def printIdealActualOutputPlot(self, fileName, pdfName):
        actualProduction = []
        idealProduction = []
        lengthArray = []
        lowest = 99999
        highest = 0
        offSet = 3816
        numberOfEntries = 24
        with open(fileName, 'rb') as csvfile:
            dat = csv.reader(csvfile, delimiter=',')
            headers = dat.next()

            i = 0
            for row in dat:
                if not "TOTAL" in row[0]:
                    i += 1
                    if i < offSet:
                        continue
                    actualProduction.append(int(float(row[0])))
                    idealProduction.append(int(float(row[1])))
                    if int(float(row[0])) < lowest:
                        lowest = int(float(row[0]))
                    if int(float(row[0])) > highest:
                        highest = int(float(row[0]))
                    if int(float(row[1])) < lowest:
                        lowest = int(float(row[1]))
                    if int(float(row[1])) > highest:
                        highest = int(float(row[1]))

                    lengthArray.append(i)
                    if i > (numberOfEntries + offSet):
                        break

        fig, ax = plt.subplots()
        fig.set_size_inches(20, 10)
        fig.subplots_adjust(bottom=0.2, right=0.95)

        #plt.axhline(14, 0, numberOfEntries, color="yellow", label="2%")
        #plt.axhline(2416, 0, numberOfEntries, color="yellow", label="2%")

        #plt.axhline(23, 0, numberOfEntries, color="purple", label="2%")
        #plt.axhline(2270, 0, numberOfEntries, color="purple", label="2%")
        #plt.axhline(31, 0, numberOfEntries, color="green", label="2%")
        #plt.axhline(2164, 0, numberOfEntries, color="green", label="2%")
        #plt.axhline(40, 0, numberOfEntries, color="blue", label="2%")
        #plt.axhline(2076, 0, numberOfEntries, color="blue", label="2%")
        #plt.axhline(49, 0, numberOfEntries, color="black", label="2%")
        #plt.axhline(2018, 0, numberOfEntries, color="black", label="2%")

        #plt.axhline(74, 0, numberOfEntries, color="purple", label="2%")
        #plt.axhline(558, 0, numberOfEntries, color="purple", label="2%")

        #plt.axhline(86, 0, numberOfEntries, color="red", label="3%")
        #plt.axhline(524, 0, numberOfEntries, color="red", label="3%")

        #plt.axhline(108, 0, numberOfEntries, color="black", label="4%")
        #plt.axhline(510, 0, numberOfEntries, color="black", label="4%")

        #plt.axhline(126, 0, numberOfEntries, color="blue", label="5%")
        #plt.axhline(502, 0, numberOfEntries, color="blue", label="5%")

        #newax.set_ticks([])
        #newax.ticks.set_visible(False)
        #newax.label.set_visible(False)

        #p1, = ax.plot(lengthArray, actualProduction, marker='s', linestyle='-', color="red",
        p1, = ax.plot(lengthArray, actualProduction, marker='o', markersize=3, linestyle='-', color="red",
                      label="Predicted Price")

        #   ax.set_xlim(1, 12)
        ax.set_xlabel('2012 Hours', color='blue')
        ax.set_ylabel('Price', color='red')
        ax.set_xlim(0 + offSet, numberOfEntries + offSet)
        ax.set_ylim(50, 450)
        #newax.set_ylim(0, 600)

        #p2, = newax.plot(lengthArray, idealProduction, marker='^', linestyle='-', color="green",
        p2, = ax.plot(lengthArray, idealProduction, marker='o', markersize=3, linestyle='-', color="green",
                      label="Actual Price")

        # newax.set_xlim(1, 12)
        #  newax.set_ylim(-10,25)

        #
        lines = [p1, p2]
        #lines = [p1]

        ax.legend(lines, [l.get_label() for l in lines])
        #newax.set_ylim([lowest - 10, highest + 10])
        #ax.set_ylim([lowest - 10, highest + 10])
        #newax.set_xlabel('Green X-axis', color='green')
        #newax.set_ylabel('Price', color='green')

        pp = PdfPages(
            #'../csvFiles/LOL.pdf')
            '../csvFiles/' + pdfName + '.pdf')
        pp.savefig(fig)
        pp.close()

    def run(self, queue, dqueue):
        nfig = queue.get()
        try:
            self.printIdealActualOutputPlot(self.fileName, self.pdfName)
            queue.task_done()
        finally:
            dqueue.put(nfig)

    def printIdealActualOutputPlotWithTwoFiles(self, fileName, fileName2, fileName3, pdfName):
        actualProduction = []
        actual2Production = []
        actual3Production = []
        idealProduction = []
        lengthArray = []
        offSet = 1000
        numberOfEntries = 1000
        useExtra = False
        if fileName3 is not "":
            useExtra = True
        with open(fileName, 'rb') as csvfile:
            dat = csv.reader(csvfile, delimiter=',')
            headers = dat.next()

            i = 0
            for row in dat:
                if not "TOTAL" in row[0]:
                    i += 1
                    if i < offSet:
                        continue
                    actualProduction.append(int(float(row[0])))
                    idealProduction.append(int(float(row[1])))

                    lengthArray.append(i)
                    if i > (numberOfEntries + offSet):
                        break

        with open(fileName2, 'rb') as csvfile:
            dat = csv.reader(csvfile, delimiter=',')
            headers = dat.next()

            i = 0
            for row in dat:
                if not "TOTAL" in row[0]:
                    i += 1
                    if i < offSet:
                        continue
                    actual2Production.append(int(float(row[0])))

                    #lengthArray.append(i)
                    if i > (numberOfEntries + offSet):
                        break

        if useExtra:
            with open(fileName3, 'rb') as csvfile:
                dat = csv.reader(csvfile, delimiter=',')
                headers = dat.next()

                i = 0
                for row in dat:
                    if not "TOTAL" in row[0]:
                        i += 1
                        if i < offSet:
                            continue
                        actual3Production.append(int(float(row[0])))

                        if i > (numberOfEntries + offSet):
                            break

        fig, ax = plt.subplots()
        fig.set_size_inches(20, 10)
        fig.subplots_adjust(bottom=0.2, right=0.95)

        #p1, = ax.plot(lengthArray, actualProduction, marker='s', linestyle='-', color="red",
        p1, = ax.plot(lengthArray, actualProduction, marker='o', markersize=3, linestyle='-', color="red",
                      label="Predicted Price(Experiment 3)")

        #   ax.set_xlim(1, 12)
        ax.set_xlabel('2012 Hours', color='blue')
        ax.set_ylabel('Price', color='red')
        ax.set_xlim(0 + offSet, numberOfEntries + offSet)
        #ax.set_ylim(0, 600)
        #newax.set_ylim(0, 600)

        #p2, = newax.plot(lengthArray, idealProduction, marker='^', linestyle='-', color="green",
        p2, = ax.plot(lengthArray, idealProduction, marker='o', markersize=3, linestyle='-', color="green",
                      label="Actual Price")

        p3, = ax.plot(lengthArray, actual2Production, marker='o', markersize=3, linestyle='-', color="blue",
                      label="Predicted Price(Experiment 2)")

        if useExtra:
            p4, = ax.plot(lengthArray, actual3Production, marker='o', markersize=3, linestyle='-', color="purple",
                          label="Predicted Price(Experiment 1)")

        if useExtra:
            lines = [p1, p2, p3, p4]
        else:
            lines = [p1, p2, p3]
        #lines = [p1]

        ax.legend(lines, [l.get_label() for l in lines])
        #newax.set_ylim([lowest - 10, highest + 10])
        #ax.set_ylim([lowest - 10, highest + 10])
        #newax.set_xlabel('Green X-axis', color='green')
        #newax.set_ylabel('Price', color='green')

        pp = PdfPages(
            #'../csvFiles/LOL.pdf')
            '../csvFiles/' + pdfName + '.pdf')
        pp.savefig(fig)
        pp.close()


def run(self, queue, dqueue):
    nfig = queue.get()
    try:
        self.printIdealActualOutputPlot(self.fileName, self.pdfName)
        queue.task_done()
    finally:
        dqueue.put(nfig)


def main():
    pathName = "../csvFiles/FilesToPlot/"

    #printer.printIdealActualOutput(pathName)
    #fileName = pathName + "StandardSet_PREDICT1369168828979.csv"
    # start threads
    fqueue = Queue()
    dqueue = Queue()

    start = datetime.now()

    threads = []
    onlyFiles = [f for f in listdir(pathName) if isfile(join(pathName, f))]
    for filename in onlyFiles:
        if "PREDICT" in filename:
            threads += [Thread(target=Plotter(pathName + filename, filename).run, args=(fqueue, dqueue))]

    i = 0
    for t in threads:
        t.daemon = True
        t.start()
        i += 1

    print i
    for fig in xrange(i):
        fqueue.put(fig)

    for _ in xrange(i):
        dqueue.get()

    for t in threads:
        t.join()

    file1 = "../csvFiles/FilesToPlot/1PTrim_X3_PAPERPrice_Consumption.csv_PREDICT1373658472788.csv"
    file2 = "../csvFiles/FilesToPlot/NoTrim_X3_PAPERPrice_Consumption.csv_PREDICT1373480735125.csv"
    #file1 = "../csvFiles/FilesToPlot/X1_1Historical_Skew_MATRIX_Price_Consump_windSpeed_temperatureRow_timeOfDay_weekdays_seasonOfYear.csv_PREDICT1371816321099.csv"
    #file2 = "../csvFiles/FilesToPlot/TEN__1PTrim_MATRIX_Price_Consump_windSpeed_temperatureRow_timeOfDay_weekdays_seasonOfYear_PREDICT1371675056079.csv"
    #file1 = "../csvFiles/FilesToPlot/X1_1Historical_Curve_Skew_PAPERMATRIX_Price_Consump_windSpeed_timeOfDay_weekdays_monthOfYear_PREDICT1371470595375.csv_PREDICT1371836733630.csv"
    file3 = ""

    printer = Plotter(file1, file1)
    printer.printIdealActualOutputPlotWithTwoFiles(file1, file2, file3, "combination")

    print datetime.now() - start


if __name__ == '__main__':
    main()