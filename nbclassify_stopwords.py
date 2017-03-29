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

def calculate_naive_bayes(classify_tokens,file_path):
    global spamFiles,hamFiles,hamWords,spamWords,vocabSize,print_fp
    prob_spam = log((spamFiles/totalFiles))
    prob_ham = log((hamFiles/totalFiles))
    for eachToken in classify_tokens:
        if eachToken in trainData['trainData'].keys():
            prob_spam += log((trainData['trainData'][eachToken]['spam'] + 1)/ (spamWords + vocabSize))
            prob_ham += log((trainData['trainData'][eachToken]['ham'] + 1)/ (hamWords + vocabSize))
    if (prob_ham >= prob_spam):
        print_output('ham',file_path)
    else:
        print_output('spam',file_path)

def classify(path):
    global print_fp

    with open('nboutput.txt',mode='w') as print_fp:
        for root,dir,files in os.walk(path,topdown=False):
            for fname in files:
                file_path = os.path.join(root,fname)
                with open(file_path,'r',encoding='latin1') as fp:
                    devData = fp.read()
                classify_tokens = devData.strip().split()
                calculate_naive_bayes(classify_tokens,file_path)

if __name__ == '__main__':
    path = sys.argv[1]
    get_training_data()
    classify(path)