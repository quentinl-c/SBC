#!/usr/bin/env python3
import collections
import random
import csv


# Global variables
posResultsForTest = 100
negResultsForTest = 1500


def write_in_file(fileContents, fileName):
    with open(fileName, 'w') as dstFile:
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

    previousCountry = -1
    currentCountry = -1

    maxLen = 1
    currentLen = 1

    for row in data:
        currentValue = row[0]
        currentCountry = row[2]
        if currentValue == previousValue and currentCountry == previousCountry:
            currentLen += 1
        else:
            maxLen = max(currentLen, maxLen)
            currentLen = 1
        previousValue = row[0]
        previousCountry = row[2]

    importantCountries = ["Canada", "United_States", "Argentina", "Cuba", "Brazil", "Mexico", "Jamaica", "Chile"]

    for row in data:
        currentValue = row[0]
        currentCountry = row[2]

        if currentValue == previousValue and currentCountry == previousCountry:
            newRow.append(row[1])
        else:
            if not len(newRow) == 0:
                temp = newRow[2]
                del newRow[2]
                for x in range(len(newRow), maxLen):
                    newRow.append('?')
                if temp in importantCountries:
                    newRow.append('America')
                else:
                    newRow.append('Other_region')
                newData.append(newRow)
                # print(newRow)
            newRow = row
            # newRow[0] = "\"" + newRow[0] + "\""
            # newRow[1] = "\"" + newRow[1] + "\""
        previousValue = row[0]
        previousCountry = row[2]

    header = ["Food"]
    for x in range(1, maxLen):
        header.append("ingr"+str(x))
    header.append("Origin")
    newData[0] = header
    return newData


def classify(content):
    posResults = []
    negResults = []
    for row in content:
        if row[-1] == 'America':
            posResults.append(row)
        else:
            negResults.append(row)
    return (posResults, negResults)


def randomize(posResults, negResults):
    trainningContent = []
    testingContent = []
    randomPosChain = get_random_chain(len(posResults))
    randomNegChain = get_random_chain(len(negResults))
    posResultsForTrain = len(posResults) - posResultsForTest
    negResultsForTrain = len(negResults) - negResultsForTest

    for i in range(0, posResultsForTrain):
        trainningContent.append(posResults[randomPosChain[i]])

    for j in range(0, negResultsForTrain):
        trainningContent.append(negResults[randomNegChain[j]])

    for i in range(posResultsForTrain, len(posResults)):
        testingContent.append(posResults[randomPosChain[i]])

    for j in range(negResultsForTrain, len(negResults)):
        testingContent.append(negResults[randomNegChain[j]])

    return (trainningContent, testingContent)


def get_random_chain(size):
    tab = [a for a in range(0, size)]
    random.shuffle(tab)
    return tab


if __name__ == '__main__':
    with open('sparqlFile', newline='') as srcFile:
        reader = csv.reader(srcFile, delimiter=' ', quotechar='|')
        cleanFileContents = clean_data(reader)
        processedFileContents = process_data(cleanFileContents)
        posResults, negResults = classify(processedFileContents)
        trainningContent, testingContent = randomize(posResults, negResults)
        write_in_file(trainningContent, 'formated_train_csv.csv')
        write_in_file(testingContent, 'formated_test_csv.csv')
        # write_in_file(cleanFileContents)
