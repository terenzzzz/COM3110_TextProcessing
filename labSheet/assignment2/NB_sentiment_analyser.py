# -*- coding: utf-8 -*-
"""
NB sentiment analyser. 

Start code.
"""
import argparse
import pandas as pd
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
import re

import string
import numpy as np



import matplotlib.pyplot as plt
import itertools
import sys

import time
from time import strftime
from time import gmtime

"""
IMPORTANT, modify this part with your details
"""
USER_ID = "acc20zj" #your unique student ID, i.e. the IDs starting with "acp", "mm" etc that you use to login into MUSE 


def parse_args():
    parser=argparse.ArgumentParser(description="A Naive Bayes Sentiment Analyser for the Rotten Tomatoes Movie Reviews dataset")
    parser.add_argument("training")
    parser.add_argument("dev")
    parser.add_argument("test")
    parser.add_argument("-classes", type=int)
    parser.add_argument('-features', type=str, default="all_words", choices=["all_words", "features"])
    parser.add_argument('-output_files', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-confusion_matrix', action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-mode', type=str, default="train", choices=["train","predict","evaluate"])
    args=parser.parse_args()
    return args

# read Phrases from file
class Phrasesor:
    def __init__(self,phraseId,sentent,sentiment):
        self.phraseId = phraseId
        self.sentent = sentent
        self.sentiment = sentiment
    
    def load(filename):
        df = pd.read_csv(filename,index_col=0, delimiter="\t")
        phrases=[]
        for index,row in df.iterrows():
            phrase = Phrasesor(index,row['Phrase'].split(),row['Sentiment'])
            phrases.append(phrase)
        return phrases
    
    def loadTest(filename):
        df = pd.read_csv(filename,index_col=0, delimiter="\t")
        phrases=[]
        for index,row in df.iterrows():
            phrase = Phrasesor(index,row['Phrase'].split(),0)
            phrases.append(phrase)
        return phrases
    

# Preprosessor
class Processor:
    def __init__(self,phrases):
        self.phrases = phrases
        # Init stopwords
        self.stoplist = []
        self.stoplist.extend(string.punctuation)
        self.stoplist = stopwords.words('english')

    def preProsess(self):
        for phrase in self.phrases:
            newSentent=set()
            for word in phrase.sentent:
                # lowerCase
                word = word.lower()
                # StopList
                if word not in self.stoplist:
                    newSentent.add(word)
            phrase.sentent = newSentent
        return self.phrases
    
    def to_3(self):
        for phrase in self.phrases:
            sentiment = phrase.sentiment
            if sentiment == 0 or sentiment == 1:
                phrase.sentiment = 0
            elif sentiment == 2:
                phrase.sentiment = 1
            elif sentiment == 3 or sentiment == 4:
                phrase.sentiment = 2
        return self.phrases
    
class FeatureSelector:
    def __init__(self,phrases):
        self.phrases = phrases
        
    def tagPhrases(self):
        for phrase in self.phrases:
            phrase.sentent = nltk.pos_tag(phrase.sentent)
            # print(phrase.sentent)
        return self.phrases 
    
    def featuresFilter(self):
        stemmer = PorterStemmer()
        self.tagPhrases()
        pattern = ["JJ", "JJR", "JJS", "RB","RBR","RBS","VB","VBD","VBG","VBN","VBP","VBZ","UH","NN","NNS","NNP","NNPS"]
        for phrase in self.phrases:
            newSentent = set()
            for word in phrase.sentent:
                if word[1] in pattern:
                    newSentent.add(stemmer.stem(word[0]))
            phrase.sentent = newSentent
        return self.phrases

# Trining     
class Trainer:
    def __init__(self, phrases,classes):
        self.phrases = phrases
        self.classes = classes
        self.class_count = self.class_count()  # 每个class的数量
        self.class_total = len(phrases)  # 所有clss的数量
        self.vocabulary = self.vocabulary()  # 出现的特征（去除重复）
        self.class_features_count = self.class_features_count() # 每个特征在每个class里面出现的次数
        self.class_featureTotal = self.class_featureTotal()  # 每个class里面出现的所有特征（包括次数）
        
    # 每个class的数量
    def class_count(self):
        class_count_dict = {} # dict: {class : count}
        
        for i in range(self.classes):
            class_count_dict[i] = 0
        
        for phrase in self.phrases:
            class_count_dict[phrase.sentiment] += 1
        # print("{class : count}",class_count_dict)
        return class_count_dict
    
    
    # 出现的特征（去除重复）
    def vocabulary(self):
        vocabulary = set()
        for phrase in self.phrases:
            for word in phrase.sentent:
                vocabulary.add(word)
        return vocabulary
    
    # 每个特征在每个class里面出现的次数
    def class_features_count(self):
        class_features_count = {}  # dict: {class : {feature:count}}
        
        for i in range(self.classes):
            class_features_count[i] = {}
        
        for phrase in self.phrases:
            for word in phrase.sentent:
                if word in class_features_count[phrase.sentiment]:
                    class_features_count[phrase.sentiment][word] += 1
                else:
                    class_features_count[phrase.sentiment][word] = 1
        return class_features_count
    
    # 每个class里面出现的所有特征（包括次数）
    def class_featureTotal(self):
        class_featureTotal = {} # dict: {class : featureTotal}
        
        for i in range(self.classes):
            class_featureTotal[i] = 0
        
        for phrases in self.phrases:
            class_featureTotal[phrases.sentiment] += len(phrases.sentent)
        # print("{class : featureTotal}:", class_featureTotal)
        return class_featureTotal
            

# Pridicting    
class Predictor:
    def __init__(self, metadata, number_classes,phrases):
        self.metadata = metadata
        self.phrases = phrases

    
    def predict(self):
        result = {}
        for phrase in self.phrases:
            likelihood_dict = {}
            for i in range(self.metadata.classes):
                # Compute Prior Probability
                prior = self.metadata.class_count[i] / self.metadata.class_total
                likelihood = prior
                # Compute Liklihood
                for word in phrase.sentent:
                    if word in self.metadata.vocabulary:
                        if word in self.metadata.class_features_count[i]:
                            count = self.metadata.class_features_count[i][word]
                        else:
                            count = 0
                        smoothed = count +1
                        smoothed_total_count = self.metadata.class_featureTotal[i] + len(self.metadata.vocabulary)
                        likelihood *= smoothed / smoothed_total_count
                likelihood_dict[i] = likelihood
            # print(likelihood_dict)
            result[phrase.phraseId] = max(likelihood_dict, key=likelihood_dict.get)
        return result
        

class Evaluator:
    def __init__(self,phrases,predictResult,sentiments_list):
        self.phrases = phrases
        self.predictResult = predictResult # {8113: 0}
        self.sentiments_list = sentiments_list
        
    
    def F1Calc(self,className):
        # for class 0
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        for phrase in self.phrases:
            if self.predictResult[phrase.phraseId] == phrase.sentiment:
                if phrase.sentiment == className:
                    TP += 1
                else:
                    TN += 1
            else:
                if phrase.sentiment == className:
                    FP += 1
                else:
                    FN += 1
        F1 = 2*TP / (2*TP + FP + FN)
        return F1
    
    def macroF1Calc(self,F1):
        macroF1 = sum(F1)/len(F1)
        return macroF1
    
    def matrix(self):
        cm = np.zeros((5,5))
        if len(self.sentiments_list) == 3:
            cm = np.zeros((3,3))
        else:
            cm = np.zeros((5,5))

        for phrase in self.phrases:
            cm[phrase.sentiment][self.predictResult[phrase.phraseId]] += 1
        
        return cm
    
            
    def plot_confusion_matrix(self, cm, title='Confusion matrix', cmap=None, normalize=True):
        
        accuracy = np.trace(cm) / float(np.sum(cm))
        misclass = 1 - accuracy
    
        if normalize:
            cm = cm.astype('float') / cm.sum()
    
        if cmap is None:
            cmap = plt.get_cmap('Blues')
    
        plt.figure(figsize=(8, 6))
        plt.imshow(cm, interpolation='nearest', cmap=cmap)
        plt.title(title)
        plt.colorbar()
    
        if self.sentiments_list is not None:
            tick_marks = np.arange(len(self.sentiments_list))
            plt.xticks(tick_marks, self.sentiments_list, rotation=45)
            plt.yticks(tick_marks, self.sentiments_list)
    
        thresh = cm.max() / 1.5 if normalize else cm.max() / 2
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            if normalize:
                plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")
            else:
                plt.text(j, i, "{:,}".format(cm[i, j]),
                         horizontalalignment="center",
                         color="white" if cm[i, j] > thresh else "black")
    
        plt.grid(False)
        plt.tight_layout()
        plt.ylabel('True label')
        plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass))
        plt.show()
    
            
def main():
    
    inputs=parse_args()
    
    #input files
    training = inputs.training
    dev = inputs.dev
    test = inputs.test
    
    #number of classes
    number_classes = inputs.classes
    
    #accepted values "features" to use your features or "all_words" to use all words (default = all_words)
    features = inputs.features
    
    #whether to save the predictions for dev and test on files (default = no files)
    output_files = inputs.output_files
     
    
    #whether to print confusion matrix (default = no confusion matrix)
    confusion_matrix = inputs.confusion_matrix
    
    model_file = "models/" + "model_class_" + str(number_classes) + "_" + str(features) + ".tsv"
    
    dev_result_file = "results/" + "dev_predictions_" + str(number_classes) + "classes_" + "acc20zj.tsv"
    
    test_result_file = "results/" +  "test_predictions_" + str(number_classes) + "classes_" + "acc20zj.tsv"
    
    
############ Init ########### 
    # Load dataset
    training_processed = Phrasesor.load(training)
    dev_processed = Phrasesor.load(dev)
    test_processed = Phrasesor.loadTest(test)
    
    # Preproccess dataset
    training_processed = Processor(training_processed).preProsess() # 74337 
    dev_processed = Processor(dev_processed).preProsess()
    test_processed = Processor(test_processed).preProsess()
    
    # Casting 5_class to 3_class if the scal is 3
    if number_classes == 3:
        # lable for confusion Matrix  
        sentiments_list = ["negative","neutral","positive"]
        
        training_processed = Processor(training_processed).to_3()
        dev_processed = Processor(dev_processed).to_3()
    else:
        sentiments_list = ["negative","somewhat negative","neutral","somewhat positive", "positive"]
        
    # Features Extraction
    if features == "features":
        featureSelector_train = FeatureSelector(training_processed)
        training_processed = featureSelector_train.featuresFilter() # 57789
        
        featureSelector_dev = FeatureSelector(dev_processed)
        dev_processed = featureSelector_dev.featuresFilter()
        
        featureSelector_test = FeatureSelector(test_processed)
        test_processed = featureSelector_test.featuresFilter()
    
    
############ Training ###########
    trained = Trainer(training_processed,number_classes)
    
    # write model to file
    with open(model_file, 'wb') as f:
            pickle.dump(trained, f)

################################## Predicting ######################################            
    # Read model from file
    with open(model_file, 'rb') as f:
        corpus_meta = pickle.load(f)
    
    # Predict
    predictor_dev = Predictor(corpus_meta,number_classes,dev_processed)
    predictResult_dev = predictor_dev.predict()

    # output predict result
    with open(dev_result_file, 'w') as f:
        f.write('SentenceId\tSentiment\n')
        for i in predictResult_dev:
                f.write(str(i) + '\t' +
                        str(predictResult_dev[i]) + '\n')
                
                
    predictor_test = Predictor(corpus_meta,number_classes,test_processed)
    predictResult_test = predictor_test.predict()

    # output predict result
    with open(test_result_file, 'w') as f:
        f.write('SentenceId\tSentiment\n')
        for i in predictResult_test:
                f.write(str(i) + '\t' +
                        str(predictResult_test[i]) + '\n')
                
################################## Evaluate ######################################
    # #Preprocessing
    # print('='*25,'Evaluation','='*25)
    predictResult = {}
    
    with open(dev_result_file, 'r') as f:
        next(f)
        for line in f:
            splited = line.split()
            predictResult[int(splited[0])] = int(splited[1])
            
    evaluator = Evaluator(dev_processed, predictResult,sentiments_list)
    
    F1_list = []
    for i in range(number_classes):
        F1_list.append(evaluator.F1Calc(i))

    macroF1 = evaluator.macroF1Calc(F1_list)
    
    print("%s\t%d\t%s\t%f" % (USER_ID, number_classes, features, macroF1))

############################## Ploting ##############################
    if confusion_matrix:
        evaluator.plot_confusion_matrix(cm =evaluator.matrix(), 
                              normalize = False,
                              title = "Confusion Matrix")
    
# ############################## Testing ##############################







if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    runtime= end -start
    runtime=strftime("%M:%S", gmtime(runtime))
    print('Running Time: ',runtime)
    sys.exit()

    