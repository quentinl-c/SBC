import collections
import csv

def write_in_file(fileContents):
    with open('formatted_sparqlFile', 'w', newline='') as dstFile:
        print("Writing in file...")
        writer = csv.writer(dstFile)
        writer.writerows(fileContents)
        print("Writing finished !")

def clean_data(data):
    newData = []

    for row in data:
        newRow = []
        for case in row:
            case = case.replace("http://dbpedia.org/resource/", "")
            case = case.replace("\"", "")
            newRow = case.split(',')
        newData.append(newRow)

    return newData

def process_data(data):
    newData = []
    newRow = []

    previousValue = -1
    currentValue = -1

    maxLen = 1
    currentLen = 1

    for row in data:
        currentValue = row[0]
        if currentValue == previousValue:
            currentLen += 1
        else:
            maxLen = max(currentLen, maxLen)
            currentLen = 1
        previousValue = row[0]

    for row in data:
        currentValue = row[0]
        if currentValue == previousValue:
            newRow.append(row[1])
        else:
            if not len(newRow) == 0:
                temp = newRow[2]
                del newRow[2]
                for x in range(len(newRow),maxLen):
                    newRow.append(None)
                newRow.append(temp)
                newData.append(newRow)
            newRow = row
        previousValue = row[0]

    header = ["Food"]
    for x in range(1,maxLen):
        header.append("ingr"+str(x))
    header.append("Origin")
    newData[0] = header
    return newData

with open('sparqlFile', newline='') as srcFile:
    reader = csv.reader(srcFile, delimiter=' ', quotechar='|')
    cleanFileContents = clean_data(reader)
    processedFileContents = process_data(cleanFileContents)
    write_in_file(processedFileContents)
