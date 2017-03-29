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
stopWords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost",
             "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount",
             "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as",
             "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand",
             "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but",
             "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail",
             "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere",
             "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few",
             "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found",
             "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he",
             "hence","her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
             "how","however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself",
             "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile",
             "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself",
             "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
             "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto",
             "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part", "per",
             "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious",
             "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow",
             "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten",
             "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby",
             "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though",
             "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards",
             "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well",
             "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby",
             "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole",
             "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours",
             "yourself", "yourselves", "the"]


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
                        if token not in stopWords:
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
                        if token not in stopWords:
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
