import os
import sys
import json
from math import log
from pprint import pprint

trainData = None
print_fp = None
totalFiles = 0
spamFiles = 0
hamFiles = 0
spamWords = 0
hamWords = 0
vocabSize = 0
classifiedHamTrue = 0
classifiedSpamTrue = 0
classifiedHamFalse = 0
classifiedSpamFalse = 0
actualHamFiles = 0
actualSpamFiles = 0



def calculate_accuracy(feature):
    precision = 1
    recall = 1
    f1Score = 1
    if 'ham' in feature:
        precision = classifiedHamTrue/(classifiedHamTrue+classifiedHamFalse)
        recall = classifiedHamTrue/(actualHamFiles)
    elif 'spam' in feature:
        precision = classifiedSpamTrue/(classifiedSpamTrue+classifiedSpamFalse)
        recall = classifiedSpamTrue/(actualSpamFiles)
    f1Score = (2*precision*recall)/(precision+recall)
    return precision*100, recall*100, f1Score*100

def print_output(label, path):
    global print_fp
    output = label + ' ' + path + '\n'
    print_fp.write(output)


def get_training_data():
    global trainData, totalFiles,spamWords,hamFiles,spamFiles, spamWords,hamWords,vocabSize
    with open('nbmodel.txt','r',encoding='latin1') as fp:
        trainData = json.loads(fp.read(),encoding='latin1')
        totalFiles = trainData['totalFilesCount']
        spamFiles = trainData['spamFilesCount']
        hamFiles = trainData['hamFilesCount']
        spamWords = trainData['spamWordsCount']
        hamWords = trainData['hamWordsCount']
        vocabSize = trainData['vocabSize']

def calculate_naive_bayes(classify_tokens, file_path, current_file):
    global spamFiles,hamFiles,hamWords,spamWords,vocabSize,print_fp,classifiedHamTrue,classifiedSpamTrue
    global classifiedHamFalse, classifiedSpamFalse
    prob_spam = log((spamFiles/totalFiles))
    prob_ham = log((hamFiles/totalFiles))
    for eachToken in classify_tokens:
        if eachToken in trainData['trainData'].keys():
            prob_spam += log((trainData['trainData'][eachToken]['spam'] + 1)/ (spamWords + vocabSize))
            prob_ham += log((trainData['trainData'][eachToken]['ham'] + 1)/ (hamWords + vocabSize))
    if (prob_ham >= prob_spam):
        print_output('ham',file_path)
        if ('ham' in current_file):
            classifiedHamTrue += 1
        else:
            classifiedHamFalse += 1
    else:
        print_output('spam',file_path)
        if ('spam' in current_file):
            classifiedSpamTrue += 1
        else:
            classifiedSpamFalse += 1

def classify(path):
    global print_fp,actualHamFiles,actualSpamFiles
    currentFile = ''
    with open('nboutput.txt',mode='w') as print_fp:
        for root,dir,files in os.walk(path,topdown=False):
            for fname in files:
                file_path = os.path.join(root,fname)
                if '\ham' in file_path:
                    actualHamFiles += 1
                    currentFile = 'ham'
                elif '\spam' in file_path:
                    actualSpamFiles += 1
                    currentFile = 'spam'
                with open(file_path,'r',encoding='latin1') as fp:
                    devData = fp.read()
                classify_tokens = devData.strip().split()
                calculate_naive_bayes(classify_tokens,file_path,currentFile)

if __name__ == '__main__':
    path = sys.argv[1]
    get_training_data()
    classify(path)
    print('Precision Recall F1 score')
    print(calculate_accuracy('ham'))
    print(calculate_accuracy('spam'))