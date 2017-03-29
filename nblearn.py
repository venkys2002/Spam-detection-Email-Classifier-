import os
import json
import sys

spamWordsCount = 0
hamWordsCount = 0
hamFilesCount = 0
spamFilesCount = 0
totalFilesCount = 0
trainData = dict()
json_Dict = dict()


def learnModel(path):
    global hamWordsCount, spamWordsCount, hamFilesCount, spamFilesCount, totalFilesCount
    for root, dir, files in os.walk(path, topdown=False):
        for fname in files:
            totalFilesCount += 1
            if "ham" in root:
                hamFilesCount += 1
                with open(os.path.join(root, fname), "r", encoding='latin1') as fp:
                    tokens = fp.read().split()
                    for token in tokens:
                        if token in trainData:
                            trainData[token]['ham'] += 1
                            hamWordsCount += 1
                        else:
                            trainData[token] = {'spam': 0, 'ham': 1}
                            hamWordsCount += 1
            elif 'spam' in root:
                spamFilesCount += 1
                with open(os.path.join(root, fname), "r", encoding='latin1') as fp:
                    fileRead = fp.read()
                    tokens = fileRead.split()
                    for token in tokens:
                        if token in trainData:
                            trainData[token]['spam'] += 1
                            spamWordsCount += 1
                        else:
                            trainData[token] = {'spam': 1, 'ham': 0}
                            spamWordsCount += 1

    lenVocab = len(trainData)
    json_Dict['trainData'] = trainData
    json_Dict['vocabSize'] = lenVocab
    json_Dict['spamWordsCount'] = spamWordsCount
    json_Dict['hamWordsCount'] = hamWordsCount
    json_Dict['hamFilesCount'] = hamFilesCount
    json_Dict['spamFilesCount'] = spamFilesCount
    json_Dict['totalFilesCount'] = totalFilesCount

    with open('nbmodel.txt', 'w') as fp:
        fp.write(json.dumps(json_Dict))


if __name__ == '__main__':
    path = sys.argv[1]
    learnModel(path)
