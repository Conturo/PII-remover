# AUTHOR: Conturo

import re, os, numpy as np, time

def read_file_names(hostFileName):
    lines = []
    fp = open(hostFileName, "r")
    for line in fp:
        line = line.strip()
        lines.append(line)
    fp.close()
    return lines

def remove_PII(inputFile, outputFile, listOfNames):
    # https://stackoverflow.com/questions/33846797/python-splitting-text-file-keeping-newlines
    words = re.findall(r'\S+|\n| ', inputFile.read())
    numReplaced = 0
    for word in words:
        #print(word)
        if (word != ' ') and (word != '\n'):
            tup = check_name(word, listOfNames)
            word = tup[0]
            numReplaced += tup[1]
        outputFile.write(word)
    return numReplaced

def attempt_autocorrect(inputWord, namesList):
    for cadetName in namesList:
        if jaccard_similarity(inputWord, cadetName) >= 0.8:
            return cadetName
    return inputWord

def jaccard_similarity(wordToCheck, dictWord):
    # https://www.statology.org/jaccard-similarity-python/
    characterSet = set(wordToCheck)
    dictWordSet = set(dictWord)
    intersectionSetCardinality = len(list(characterSet.intersection(dictWordSet)))
    # print(intersectionCardinality)
    intersectionCardinality = len([i for i in list(wordToCheck) if i in list(dictWord)])
    # print(intersectionCardinality)
    unionCardinality = (len(characterSet) + len(dictWordSet)) - intersectionSetCardinality
    return float(intersectionCardinality) / unionCardinality
    

def check_name(wordToCheck, listOfNames):
    namesReplaced = 0
    # nameNum = 0
    if wordToCheck in listOfNames:
        wordToCheck = "<NAME>"
        namesReplaced = 1
    # for name in listOfNames:
    #     nameNum+=1
    #     if name.lower() == wordToCheck.lower():
    #         wordToCheck = "<NAME>"
    #         namesReplaced = 1
    #     else:
    #         wordToCheck = attempt_autocorrect(wordToCheck, listOfNames)
    return wordToCheck, namesReplaced


# MAIN
def mainOne():
    start_time = time.time()
    fileNames = read_file_names("hostFile.txt")
    dictFile = open("nameList.txt", "r")
    dictFileString = dictFile.read()
    cadetNames = dictFileString.split()
    dictCadetNames = dict.fromkeys(cadetNames, 1)
    for eachFile in fileNames:
        input = open(eachFile, "r")
        outputFileName = eachFile.replace(".txt", "Output.txt")
        output = open(outputFileName, "w+")
        remove_PII(input, output, dictCadetNames)
        input.close()
        output.close()
    dictFile.close()
    print("--- %s seconds ---" % (time.time() - start_time))

def mainTwo():
    start_time = time.time()
    dictFile = open("names.txt", "r")
    dictFileString = dictFile.read()
    cadetNames = dictFileString.split()
    for filename in os.listdir("lsn1_helloworld"):
        with open(os.path.join("lsn1_helloworld", filename), 'r') as input:
            outputFileName = filename.replace(".txt", "Output.txt")
            outputFileName = os.path.join("lsn1_helloworld_out", outputFileName)
            output = open(outputFileName, "w+")
            numReplaced = remove_PII(input, output, cadetNames)
            input.close()
            output.close()
            print(filename, "successfully scanned |", numReplaced, "name(s) censored")
    dictFile.close()
    print("--- %s seconds ---" % (time.time() - start_time))


mainTwo()
