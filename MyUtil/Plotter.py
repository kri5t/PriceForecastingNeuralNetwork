import csv
from os import listdir
from os.path import isfile, join
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


class Plotter():
    def __init__(self):
        """ Init method """

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
        numberOfEntries = 1000
        with open(fileName, 'rb') as csvfile:
            dat = csv.reader(csvfile, delimiter=',')
            headers = dat.next()

            i = 0
            for row in dat:
                if not "TOTAL" in row[0]:
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

                    i += 1
                    lengthArray.append(i)
                    if i > numberOfEntries:
                        break

        fig, ax = plt.subplots()
        fig.set_size_inches(20, 10)
        fig.subplots_adjust(bottom=0.2, right=0.95)

        #plt.axhline(61, 0, 1600)
        #plt.axhline(632, 0, 1600)

        newax = fig.add_axes(ax.get_position())
        newax.patch.set_visible(False)
        #newax.set_ticks([])
        #newax.ticks.set_visible(False)
        #newax.label.set_visible(False)
        newax.yaxis.set_label_position('right')
        newax.yaxis.set_ticks_position('right')

        #p1, = ax.plot(lengthArray, actualProduction, marker='s', linestyle='-', color="red",
        p1, = ax.plot(lengthArray, actualProduction, marker='o', markersize=3, linestyle='-', color="red",
                      label="Predicted Price")
        # ax.set_ylim(85,115)
        #   ax.set_xlim(1, 12)
        ax.set_xlabel('2012 Hours', color='blue')
        ax.set_ylabel('Price', color='red')
        ax.set_xlim(0, numberOfEntries)
        newax.set_xlim(0, numberOfEntries)


        #p2, = newax.plot(lengthArray, idealProduction, marker='^', linestyle='-', color="green",
        p2, = newax.plot(lengthArray, idealProduction, marker='o', markersize=3, linestyle='-', color="green",
                         label="Actual Price")

        # newax.set_xlim(1, 12)
        #  newax.set_ylim(-10,25)

        #
        lines = [p1, p2]
        #lines = [p1]

        ax.legend(lines, [l.get_label() for l in lines])
        newax.set_ylim([lowest - 10, highest + 10])
        ax.set_ylim([lowest - 10, highest + 10])
        #newax.set_xlabel('Green X-axis', color='green')
        #newax.set_ylabel('Price', color='green')

        pp = PdfPages(
            #'../csvFiles/LOL.pdf')
            '../csvFiles/' + pdfName + '.pdf')
        pp.savefig(fig)
        pp.close()


def main():
    pathName = "../csvFiles/FilesToPlot/"
    printer = Plotter()
    #printer.printIdealActualOutput(pathName)
    #fileName = pathName + "StandardSet_PREDICT1369168828979.csv"
    onlyFiles = [f for f in listdir(pathName) if isfile(join(pathName, f))]
    for filename in onlyFiles:
        if "24HOUR" in filename:
            #print "ok"
            printer.printIdealActualOutputPlot(pathName + filename, filename)


if __name__ == '__main__':
    main()