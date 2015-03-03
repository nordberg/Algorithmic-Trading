import csv
import itertools

def getHistData(filename):
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')

        data = []
        symbs = []
        i = 0
        for row in reader:
            if i == 1:
                for symb in row:
                    symbs.append(symb)
            day = {}

            if i > 1:
                for j in range(0, len(symbs) - 1):
                    day[symbs[j]] = row[j]
                data.append(day)
            i += 1
    return data

#print getHistData('ERIC-A.csv')