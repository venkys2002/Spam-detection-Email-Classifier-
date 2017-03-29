import os,sys,random,json
from collections import defaultdict

filename_dict = dict()
filelist = []
feature_weights = defaultdict(int)
json_dict = defaultdict()

def get_filenames(path):
    global filename_dict,filelist,feature_weights
    for root, dir, files in os.walk(path, topdown=False):
        for fname in files:
            if "ham" in root:
                with open(os.path.join(root, fname), "r", encoding='latin1') as fp:
                    tokens = fp.read().split()
                    #Cache the file contents for faster processing
                    filename_dict[fname] = {'label': -1, 'tokens': tokens}
                    #Create a list of filenames for randomizing
                    filelist.append(fname)
            elif 'spam' in root:
                with open(os.path.join(root, fname), "r", encoding='latin1') as fp:
                    tokens = fp.read().split()
                    filename_dict[fname] = {'label': 1, 'tokens': tokens}
                    filelist.append(fname)
    # json_dict['updated_bias'] = 0
    return

def learn_model():
    global filelist,feature_weights,filename_dict,json_dict
    bias = 0
    for i in range(0,20):
        random.shuffle(filelist)
        for file in filelist:
            alpha = 0
            y = filename_dict[file]['label']
            feature_list = filename_dict[file]['tokens']
            #Calculate the activation value for the Current file
            for feature in feature_list:
                alpha += feature_weights[feature]
            alpha += bias

            if((y*alpha) <= 0):
                for feature in feature_list:
                    feature_weights[feature] += y
                bias += y
    json_dict = {'updated_bias': bias, 'feature_weights': feature_weights}


if __name__ == '__main__':
    path = sys.argv[1]
    get_filenames(path)
    learn_model()
    with open('per_model.txt', 'w') as fp:
        fp.write(json.dumps(json_dict))