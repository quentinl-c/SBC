import collections
import csv

def write_in_file(fileContents):
    with open('formatted_sparqlFile.csv', 'w') as dstFile:
        print("Writing in file...")
        writer = csv.writer(dstFile, quotechar="'")
        writer.writerows(fileContents)
        print("Writing finished !")

def clean_data(data):
    newData = []

    for row in data:
        newRow = []
        for case in row:
            case = case.replace("http://dbpedia.org/resource/", "")
            case = case.replace("\"", "")
            case = case.replace("\'", "")
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

    importantCountries = ["\"Canada\"", "\"United_States\""]

    for row in data:
        currentValue = row[0]

        if currentValue == previousValue:
            newRow.append(row[1])
        else:
            if not len(newRow) == 0:
                temp = newRow[2]
                del newRow[2]
                for x in range(len(newRow),maxLen):
                    newRow.append('')
                if temp in importantCountries:
                    newRow.append('Northern_America')
                else:
                    newRow.append('Other_region')
                newData.append(newRow)
                #print(newRow)
            newRow = row
            #newRow[0] = "\"" + newRow[0] + "\""
            #newRow[1] = "\"" + newRow[1] + "\""
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
