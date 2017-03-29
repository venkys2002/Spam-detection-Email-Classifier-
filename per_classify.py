import os,sys,json

def classify(path,output):

    with open('per_model_final.txt',mode='r',encoding='latin1') as fptr:
        train_data = json.loads(fptr.read(),encoding="latin1")
        feature_weights = train_data['feature_weights']
        updated_bias = train_data['updated_bias']
    with open(output,mode='w') as fw_ptr:
        for root, dir, files in os.walk(path,topdown=False):
            for fname in files:
                alpha = 0
                file_path = os.path.join(root,fname)
                with open(os.path.join(root, fname), "r", encoding='latin1') as fp:
                    tokens = fp.read().split()
                    for each_token in tokens:
                        if each_token in feature_weights:
                            alpha += feature_weights[each_token]
                    alpha += updated_bias
                if( alpha > 0):
                    classify_file = "spam "+file_path+"\n"
                    fw_ptr.write(classify_file)
                else:
                    classify_file = "ham "+file_path+"\n"
                    fw_ptr.write(classify_file)

if __name__ == '__main__':
    input_path = sys.argv[1]
    output_filename = sys.argv[2]
    classify(input_path,output_filename)