# -*- coding: utf-8 -*-
"""
NB sentiment analyser. 

Start code.
"""
import argparse
import pandas as pd
import pickle

from nltk.corpus import stopwords
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
    
    def preProsess(self):
        for phrase in self.phrases:
            newSentent=[]
            for word in phrase.sentent:
                # lowerCase
                word = word.lower()
                # StopList
                if word not in stopwords.words('english'):
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
    def __init__(self, metadata, classes):
        self.metadata = metadata
        self.classes = classes
        
    def predict(self,phrases):
        # Final predict class = max(PriorProbability * sum of features likelyhood)
        
        result = {}      # dict: {phraseId : sentiment}  
        class_prediction = {} #dict: {class : prediction}
        
        for i in range(self.classes):
            class_prediction[i] = 0
        
        
        for phrase in phrases:
            for i in range(self.classes):
                predict = self.metadata.prior[i]
                for word in phrase.sentent:
                    if word in self.metadata.vocabulary():
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
    

################################## Training ######################################
    #Preprocessing
    # print('='*50,' Training','='*50)
    # phrases = Phrasesor.load(training)
    # processed = Processor(phrases).preProsess()
    # if number_classes == 5:
    #     phrases_scaled = processed
    # else:
    #     phrases_scaled = Processor(processed).to_3()


    # # Training
    # trainer = Trainer(phrases_scaled,number_classes)

    # with open('Training_model', 'wb') as f:
    #         pickle.dump(trainer, f)

    # print()
    # print('='*50,'Trainning Result','='*50)
    # for i in trainer.prior:
    #     print(i,trainer.prior[i])
    
################################## Developing ######################################
    # load model
    with open('Training_model', 'rb') as f:
        corpus_meta = pickle.load(f)
    predictor = Predictor(corpus_meta,number_classes)
    
    # #Preprocessing
    phrases = Phrasesor.load(dev)
    processed = Processor(phrases).preProsess()
    to3Class = Processor(processed).to_3()
    predictResult = predictor.predict(to3Class)
    # print(predictResult)
    with open("result", 'w') as f:
        f.write('SentenceId\tSentiment\n')
        for i in predictResult:
                f.write(str(i) + '\t' +
                        str(predictResult[i]) + '\n')
                
################################## Evaluate ######################################
    #Preprocessing
    evaluator = Evaluator(to3Class,predictResult)
    F1_0 = evaluator.F1Calc(0)
    F1_1 = evaluator.F1Calc(1)
    F1_2 = evaluator.F1Calc(2)
    print(F1_0,F1_1,F1_2)
    macroF1 = evaluator.macroF1Calc([F1_0,F1_1,F1_2])
    
    macroF1 = 0


    """
    IMPORTANT: your code should return the lines below. 
    However, make sure you are also implementing a function to save the class predictions on dev and test sets as specified in the assignment handout
    """
    #print("Student\tNumber of classes\tFeatures\tmacro-F1(dev)\tAccuracy(dev)")
    print()
    print('='*50,'Evaluation','='*50)
    print("%s\t%d\t%s\t%f" % (USER_ID, number_classes, features, macroF1))

if __name__ == "__main__":
    main()