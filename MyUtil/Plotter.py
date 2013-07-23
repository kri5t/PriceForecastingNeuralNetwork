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

    def printIdealActualOutputPlot(self, fileName, pdfName, lines):
        actualProduction = []
        idealProduction = []
        lengthArray = []
        lowest = 99999
        highest = 0
        offSet = 3
        numberOfEntries = 250
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

        font = {'family': 'sans-serif', 'size': 20}

        plt.rc('font', **font)

        plt.rc('xtick', labelsize=22)
        plt.rc('ytick', labelsize=22)

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
        if lines != 0:
            for i in range(4, numberOfEntries, lines):
                plt.axvline(i, 0, 700, color="black")
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
        #ax.set_ylim(0, 500)
        ax.set_ylim(0, 700)

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

    def printActualErrorOutputPlot(self, fileName):
        actualProduction = []
        idealProduction = []
        error = []
        lengthArray = []
        lowest = 99999
        highest = 0
        offSet = 0
        numberOfEntries = 250
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
                    error.append(abs(int(float(row[1])) - int(float(row[0]))))

                    lengthArray.append(i)
                    if i > (numberOfEntries + offSet):
                        break

        font = {'family': 'sans-serif', 'size': 20}

        plt.rc('font', **font)

        plt.rc('xtick', labelsize=22)
        plt.rc('ytick', labelsize=22)

        fig, ax = plt.subplots()
        fig.set_size_inches(20, 10)
        fig.subplots_adjust(bottom=0.2, right=0.95)

        #newax = fig.add_axes(ax.get_position())
        #newax.patch.set_visible(False)

        #newax.yaxis.set_label_position('right')
        #newax.yaxis.set_ticks_position('right')

        p1, = ax.plot(lengthArray, actualProduction, marker='o', markersize=3, linestyle='-', color="red",
                      label="Predicted Price")

        #   ax.set_xlim(1, 12)
        ax.set_xlabel('2012 Hours', color='blue')
        ax.set_ylabel('Price', color='red')
        ax.set_xlim(0 + offSet, numberOfEntries + offSet)
        #newax.set_xlabel('2012 Hours', color='blue')
        #newax.set_ylabel('MAE', color='black')
        #newax.set_xlim(0 + offSet, numberOfEntries + offSet)
        #newax.set_ylim(0, 1500)
        ax.set_ylim(0, 600)

        p2, = ax.plot(lengthArray, idealProduction, marker='o', markersize=3, linestyle='-', color="green",
                      label="Actual Price")
        p3, = ax.plot(lengthArray, error, marker='o', markersize=3, linestyle='-', color="black",
                         label="MAE")

        lines = [p1, p2, p3]
        #lines = [p1]

        ax.legend(lines, [l.get_label() for l in lines])
        #newax.legend(lines, [l.get_label() for l in lines])
        #ax.set_ylim([lowest - 10, highest + 10])

        pp = PdfPages(
            #'../csvFiles/LOL.pdf')
            '../csvFiles/' + fileName.replace(".csv", "") + '.pdf')
        pp.savefig(fig)
        pp.close()

    def printRows(self, fileName, row1, row2, row1Label, row2Label):
        actualProduction = []
        idealProduction = []
        lengthArray = []
        offSet = 0
        numberOfEntries = 500
        with open(fileName, 'rb') as csvfile:
            dat = csv.reader(csvfile, delimiter=',')
            headers = dat.next()

            i = 0
            for row in dat:
                if not "TOTAL" in row[0]:
                    i += 1
                    if i < offSet:
                        continue
                    actualProduction.append(int(float(row[row1])))
                    idealProduction.append(int(float(row[row2])))

                    lengthArray.append(i)
                    if i > (numberOfEntries + offSet):
                        break

        font = {'family': 'sans-serif', 'size': 20}

        plt.rc('font', **font)

        plt.rc('xtick', labelsize=22)
        plt.rc('ytick', labelsize=22)

        fig, ax = plt.subplots()
        fig.set_size_inches(20, 10)
        fig.subplots_adjust(bottom=0.2, right=0.95)

        newax = fig.add_axes(ax.get_position())
        #newax.patch.set_visible(False)
        newax.patch.set_visible(False)

        newax.yaxis.set_label_position('right')
        newax.yaxis.set_ticks_position('right')

        p1, = ax.plot(lengthArray, actualProduction, marker='o', markersize=3, linestyle='-', color="red",
                      label=row1Label)

        #newax.set_ticks([])

        #   ax.set_xlim(1, 12)
        ax.set_xlabel('2012 Hours', color='blue')
        ax.set_ylabel(row1Label, color='red')
        newax.set_ylabel(row2Label, color='green')
        ax.set_xlim(0 + offSet, numberOfEntries + offSet)
        #newax.set_xlabel('2012 Hours', color='blue')
        #newax.set_ylabel('MAE', color='black')
        newax.set_xlim(0 + offSet, numberOfEntries + offSet)
        ax.set_ylim(1000, 5000)
        #ax.set_ylim(0, 600)

        p2, = newax.plot(lengthArray, idealProduction, marker='o', markersize=3, linestyle='-', color="green",
                         label=row2Label)

        lines = [p1, p2]
        #lines = [p1]

        #newax.ticks.set_visible(False)
        #newax.label.set_visible(False)
        ax.legend(lines, [l.get_label() for l in lines])
        newax.legend(lines, [l.get_label() for l in lines])
        #ax.set_ylim([lowest - 10, highest + 10])

        pp = PdfPages(
            '../csvFiles/' + fileName.replace(".csv", "1") + '.pdf')
        pp.savefig(fig)
        pp.close()

    def run(self, queue, dqueue, lines):
        nfig = queue.get()
        try:
            self.printIdealActualOutputPlot(self.fileName, self.pdfName, lines)
            queue.task_done()
        finally:
            dqueue.put(nfig)

    def printIdealActualOutputPlotWithTwoFiles(self, fileName, fileName2, fileName3, pdfName,
                                               label1, label2, offSet, numberOfHours):
        actualProduction = []
        actual2Production = []
        actual3Production = []
        idealProduction = []
        lengthArray = []
        numberOfEntries = numberOfHours
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
        font = {'family': 'sans-serif', 'size': 14}

        plt.rc('font', **font)

        plt.rc('xtick', labelsize=22)
        plt.rc('ytick', labelsize=22)
        #p1, = ax.plot(lengthArray, actualProduction, marker='s', linestyle='-', color="red",

        #   ax.set_xlim(1, 12)
        ax.set_xlabel('2012 Hours', color='blue')
        ax.set_ylabel('Price', color='red')
        ax.set_xlim(0 + offSet, numberOfEntries + offSet)
        #ax.set_ylim(0, 600)
        #newax.set_ylim(0, 600)

        #p2, = newax.plot(lengthArray, idealProduction, marker='^', linestyle='-', color="green",
        actual, = ax.plot(lengthArray, idealProduction, marker='o', markersize=3, linestyle='-', color="green",
                          label="Actual Price")

        f1, = ax.plot(lengthArray, actualProduction, marker='o', markersize=3, linestyle='-', color="red",
                      #label="#55 prediction")
                      label=label1)

        f2, = ax.plot(lengthArray, actual2Production, marker='o', markersize=3, linestyle='-', color="blue",
                      #label="#1 prediction")
                      label=label2)

        if useExtra:
            f3, = ax.plot(lengthArray, actual3Production, marker='o', markersize=3, linestyle='-', color="purple",
                          label="Without DoW")

        if useExtra:
            lines = [f1, f2, f3, actual]
        else:
            lines = [f1, f2, actual]
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
    """


    """
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
        if "PREDICT" in filename and "pdf" not in filename:
            if "HourAhead" in filename:
                lines = int(filename.split("HourAhead")[0])
                if lines > 5:
                    threads += [Thread(target=Plotter(pathName + filename, filename).run, args=(fqueue, dqueue, lines))]
                else:
                    threads += [Thread(target=Plotter(pathName + filename, filename).run, args=(fqueue, dqueue, 0))]
            else:
                threads += [Thread(target=Plotter(pathName + filename, filename).run, args=(fqueue, dqueue, 24))]

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


    file3 = ""
    file1 = "../csvFiles/FilesToPlot/NEWQuarterTrain_MATRIX_Price_Consump_windSpeed_temperatureRow_weekdays_seasonOfYear_PREDICT1371470088413.csv"
    file2 = "../csvFiles/FilesToPlot/NEWQuarterTrain_MATRIX_Price_Consump_windSpeed_temperatureRow_timeOfDay_weekdays_seasonOfYear_PREDICT1371469803190.csv"
    printer = Plotter(file1, file1)
    printer.printRows("../csvFiles/YEAR_2011_2012_DA_EXCEL_FOR_DA_PRICE_FORECAST_06-05-2013_CORRECTED_DATA.csv", 2, 5, "Consumption", "Price")
    #printer.printIdealActualOutputPlotWithTwoFiles(file1, file2, file3, "combination", label1="", label2="", offSet="",
     #                                              numberOfHours="")

    file1 = "../csvFiles/FilesToPlot/2StandardRun_MATRIX_Price_Consump_windSpeed_temperatureRow_timeOfDay_weekdays_seasonOfYear.csv_PREDICT1374146770980.csv"
    file2 = "../csvFiles/FilesToPlot/200EPOCHS_MATRIX_Price_Consump_windSpeed_temperatureRow_timeOfDay_weekdays_seasonOfYear.csv_PREDICT1373486968046.csv"
    printer.printIdealActualOutputPlotWithTwoFiles(file1, file2, file3, "X2_X3_Best_Comb_3800_4000",
                                                   label1="New",
                                                   label2="Old", offSet=0,
                                                   numberOfHours=250)
    #file1 = "../csvFiles/FilesToPlot/X1_1Historical_Curve_Skew_PAPERMATRIX_Price_Consump_windSpeed_timeOfDay_weekdays_monthOfYear_PREDICT1371470595375.csv_PREDICT1371836733630.csv"
    #file3 = "../csvFiles/FilesToPlot/NEWQuarterTrain_MIXEDPrice_Consump_windSpeed_temperatureRow_weekdays_seasonOfYearMATRIX_PREDICT1371562034544.csv"



    printer.printActualErrorOutputPlot("../csvFiles/FilesToPlot/X1_1Historical_Skew_MATRIX_Price_Consump_windSpeed_temperatureRow_timeOfDay_weekdays_seasonOfYear.csv_PREDICT1371816321099.csv")

    print datetime.now() - start


if __name__ == '__main__':
    main()