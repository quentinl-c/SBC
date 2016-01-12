#!/usr/bin/env python3
import collections
import random
import csv


# Global variables
posResultsForTrain = 1000
negResultsForTrain = 1000


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

    # importantCountries = ["Canada", "United_States", "Argentina", "Cuba", "Brazil", "Mexico", "Jamaica", "Chile"]
    importantCountries = ["Canada", "United_States", "France", "England", "Scotland", "Australia", "Germany", "Italy", "Spain", "Russia", "Poland", "Denmark", "Slovakia", "Estonia", "Lithuania", "Belgium", "Austria", "Bulgaria", "Czech_Republic", "Croatia", "Cyprus", "Malta", "Greece", "Hungary", "Ireland", "Slovenia", "Sweden", "United_Kingdom", "Portugal", "Luxembourg", "Latvia", "Albania", "Montenegro", "Serbia", "Kosovo", "Bosnia_and_Herzegovina"]
    counter = 0
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
                    newRow.append('Occidental')
                    counter += 1
                else:
                    newRow.append('Other_region')
                newData.append(newRow)
                # print(newRow)
            newRow = row
            # newRow[0] = "\"" + newRow[0] + "\""
            # newRow[1] = "\"" + newRow[1] + "\""
        previousValue = row[0]
        previousCountry = row[2]
    #print(counter)

    header = ["Food"]
    for x in range(1, maxLen):
        header.append("ingr"+str(x))
    header.append("Origin")
    newData[0] = header
    return newData


def classify(content):
    head = content.pop(0)
    posResults = []
    negResults = []
    for row in content:
        if row[-1] == 'Occidental':
            posResults.append(row)
        else:
            negResults.append(row)
    print(len(posResults))
    print(len(negResults))
    return (head, posResults, negResults)

def classifyNumberIngredients(content):
    head = content.pop(0)
    for i in range (5, len(head)-1):
        del head[5]
    size = 0
    posResults = []
    negResults = []
    for row in content:
        size = 0
        for i in range(1, len(row)-1):
            if row[i] == "?":
                break
            else:
                size += 1
        if size <= 5:
            for i in range (5, len(row)-1):
                    del row[5]
            if row[-1] == 'Occidental':
                posResults.append(row)
            else:
                negResults.append(row)
    print(len(posResults))
    print(len(negResults))
    return (head, posResults, negResults)

def randomize(head, posResults, negResults):
    trainningContent = []
    testingContent = []
    randomPosChain = get_random_chain(len(posResults))
    randomNegChain = get_random_chain(len(negResults))
    posResultsForTest = len(posResults) - posResultsForTrain
    negResultsForTest = len(negResults) - negResultsForTrain

    for i in range(0, posResultsForTrain):
        trainningContent.append(posResults[randomPosChain[i]])

    for j in range(0, negResultsForTrain):
        trainningContent.append(negResults[randomNegChain[j]])

    for i in range(posResultsForTrain, len(posResults)):
        testingContent.append(posResults[randomPosChain[i]])

    for j in range(negResultsForTrain, len(negResults)):
        testingContent.append(negResults[randomNegChain[j]])

    random.shuffle(trainningContent)
    random.shuffle(testingContent)

    trainningContent.insert(0, head)
    testingContent.insert(0, head)

    return (trainningContent, testingContent)

def get_random_chain(size):
    tab = [a for a in range(0, size)]
    random.shuffle(tab)
    return tab

if __name__ == '__main__':
    with open('sparqlFile', newline='') as srcFile:
        reader = csv.reader(srcFile, delimiter=' ', quotechar='|')
        cleanFileContents = clean_data(reader)
        write_in_file(cleanFileContents, 'clean.csv')
        processedFileContents = process_data(cleanFileContents)
        head, posResults, negResults = classifyNumberIngredients(processedFileContents)
        trainningContent, testingContent = randomize(head, posResults, negResults)
        write_in_file(trainningContent, 'formated_train_csv.csv')
        write_in_file(testingContent, 'formated_test_csv.csv')
        # write_in_file(cleanFileContents)
