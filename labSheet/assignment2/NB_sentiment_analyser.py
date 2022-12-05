# -*- coding: utf-8 -*-
"""
NB sentiment analyser. 

Start code.
"""
import argparse
import pandas as pd
import pickle
import regex as re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import numpy as np

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
    

# Preprosessor
class Processor:
    def __init__(self,phrases):
        self.phrases = phrases
        # Init stopwords
        self.stoplist = []
        with open('stop_list.txt') as f:
            for word in f:
                self.stoplist.append(word)
        self.stoplist.extend(string.punctuation)
        self.stoplist = set(self.stoplist)

    
    def preProsess(self):
        for phrase in self.phrases:
            newSentent=[]
            for word in phrase.sentent:
                # lowerCase
                word = word.lower()
                # StopList
                if word not in self.stoplist:
                    newSentent.append(word)
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
        return self.phrases 
    
    def featuresFilter(self):
        self.tagPhrases()
        pattern = ["JJ", "RB", "JJR", "JJS"]
        for phrase in self.phrases:
            newSentent = []
            for word in phrase.sentent:
                if word[1] in pattern:
                    newSentent.append(word[0])
            phrase.sentent = newSentent
        return self.phrases
                    

# Trining     
class Trainer:
    def __init__(self, phrases,classes):
        self.phrases = phrases
        self.classes = classes
        self.prior = self.class_prior()
        self.likelihood = self.class_feature_likelihood()

    def class_count(self):
        class_count_dict = {} # dict: {class : count}
        for i in range(self.classes):
            class_count_dict[i] = 0
        
        for phrase in self.phrases:
            class_count_dict[phrase.sentiment] += 1
        return class_count_dict
    
    def class_prior(self):
        class_prior_dict = {} # dict: {class : priorProbabiliry}
        total_class_count = 0
        
        class_count_dict = self.class_count()
        for i in class_count_dict:
            total_class_count += class_count_dict[i]
            
        for i in range(self.classes):
            class_prior_dict[i] = 0
        
        for i in class_count_dict:
            class_prior_dict[i] = class_count_dict[i]/total_class_count
        return class_prior_dict
        
    def vocabulary(self):
        vocabulary = set()
        for phrase in self.phrases:
            for word in phrase.sentent:
                vocabulary.add(word)
        return vocabulary
    
    
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
    
    def class_featureTotal(self):
        class_featureTotal = {} # dict: {class : featureTotal}
        
        for i in range(self.classes):
            class_featureTotal[i] = 0
            
        class_features_count = self.class_features_count()
        
        for sentiment in class_features_count: # dict: {class : {feature:count}}
            class_featureTotal[sentiment] += len(class_features_count[sentiment])
        return class_featureTotal
    
    def class_feature_likelihood(self):
        class_feature_likelihood = {} # dict: {class : {feature:likelihood}}
        for i in range(self.classes):
            class_feature_likelihood[i] = {}
            
        class_features_count = self.class_features_count()
        class_featureTotal = self.class_featureTotal()
        vocabulary_count = len(self.vocabulary())
        
        
        for phrase in self.phrases:
            for word in phrase.sentent:
                likelihood = (class_features_count[phrase.sentiment][word] + 1)/(class_featureTotal[phrase.sentiment] + vocabulary_count)
                class_feature_likelihood[phrase.sentiment][word]=likelihood
        return class_feature_likelihood
            

# Pridicting    
class Predictor:
    def __init__(self, metadata, number_classes,phrases):
        self.metadata = metadata
        self.number_classes = number_classes
        self.phrases = phrases
        self.result = self.predict()
        
    def predict(self):
        # Final predict class = max(PriorProbability * sum of features likelyhood)
        result = {}      # dict: {phraseId : sentiment}  
        class_prediction = {} #dict: {class : prediction}
        
        for i in range(self.number_classes):
            class_prediction[i] = 0
        
        for phrase in self.phrases:
            for i in range(self.number_classes):
                predict = self.metadata.prior[i]
                for word in phrase.sentent:
                    if word in self.metadata.likelihood[i]:
                        predict *= self.metadata.likelihood[i][word]
                class_prediction[i] = predict
            result[phrase.phraseId] = max(class_prediction, key=class_prediction.get)
            
        return result

class Evaluator:
    def __init__(self,phrases,predictResult):
        self.phrases = phrases
        self.predictResult = predictResult
    
    def F1Calc(self,className):
        # for class 0
        TP = 0
        FP = 0
        FN = 0
        for phrase in self.phrases:
            if self.predictResult[phrase.phraseId] == phrase.sentiment:
                if phrase.sentiment == className:
                    TP += 1
            else:
                if phrase.sentiment == className:
                    FP += 1
                else:
                    FN += 1
        F1 = 2*TP / (2*TP + FP + FN)
        return F1
    
    def macroF1Calc(self,F1):
        N = len(F1)
        total = 0
        for i in range(N):
            total += F1[i]
        macroF1 = 1/N * total
        return macroF1
    
class confusion_matrix_Ploter:
    def __init__(self,number_classes):
        # Sentiment values
        self.sentiments_list = ["negative","somewhat negative","neutral","somewhat positive", "positive"]
        if number_classes == 3:
            self.sentiments_list = ["negative","neutral","positive"]
            
    def plot_confusion_matrix(self, cm, title='Confusion matrix', cmap=None, normalize=True):
        import matplotlib.pyplot as plt
        import numpy as np
        import itertools
    
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
    
    mode = inputs.mode
    
    model_file = "Trained model_class_" + str(number_classes)
    result_file = "Predict_class_" + str(number_classes)
    
    
############ Init ###########   
    print('='*25,' Init','='*25)
    training_processed = Phrasesor.load(training)
    dev_processed = Phrasesor.load(dev)
    
    training_processed = Processor(training_processed).preProsess()
    dev_processed = Processor(dev_processed).preProsess()
    
    if number_classes == 3:
        training_processed = Processor(training_processed).to_3()
        dev_processed = Processor(dev_processed).to_3()
        
    if features == "features":
        featureSelector = FeatureSelector(training_processed)
        training_processed = featureSelector.featuresFilter()
    
    
############ Training ###########
    #Preprocessing
    print('='*25,' Training','='*25)
    
    # Training
    print("Training in Process...")
    trainer = Trainer(training_processed,number_classes)

    with open(model_file, 'wb') as f:
            pickle.dump(trainer, f)
    print()
    print('-'*25,'Trainning Result','-'*25)
    for i in trainer.prior:
        print(i,trainer.prior[i])

################################## Predicting ######################################            
    print('='*25,'Predict','='*25)
    with open(model_file, 'rb') as f:
        corpus_meta = pickle.load(f)

    print("Predicting in Process...")
    predictor = Predictor(corpus_meta,number_classes,dev_processed)
    predictResult = predictor.result

    # output predict result
    with open(result_file, 'w') as f:
        f.write('SentenceId\tSentiment\n')
        for i in predictResult:
                f.write(str(i) + '\t' +
                        str(predictResult[i]) + '\n')
                
################################## Evaluate ######################################
    # #Preprocessing
    print('='*25,'Evaluation','='*25)
    predictResult = {}
    
    result_file
    with open(result_file, 'r') as f:
        next(f)
        for line in f:
            splited = line.split()
            predictResult[int(splited[0])] = int(splited[1])
    #Preprocessing
    print("Evaluating in Process...")
    evaluator = Evaluator(dev_processed, predictResult)
    F1_list = []
    for i in range(number_classes):
        F1_list.append(evaluator.F1Calc(i))

    macroF1 = evaluator.macroF1Calc(F1_list)
    
    print("%s\t%d\t%s\t%f" % (USER_ID, number_classes, features, macroF1))

############################## Testing ##############################

############################## Ploting ##############################
    ploter = confusion_matrix_Ploter(number_classes)
        
    cm = np.zeros((5,5))
    sentiments_list = ["negative","somewhat negative","neutral","somewhat positive", "positive"]
    if number_classes == 3:
        cm = np.zeros((3,3))
        sentiments_list = ["negative","neutral","positive"]
    
    ploter.plot_confusion_matrix(cm           = cm, 
                          normalize    = False,
                          title        = "Confusion Matrix")

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    runtime= end -start
    runtime=strftime("%H:%M:%S", gmtime(runtime))
    print('Running Time: ',runtime)

    