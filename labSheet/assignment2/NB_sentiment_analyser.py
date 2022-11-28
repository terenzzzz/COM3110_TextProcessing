# -*- coding: utf-8 -*-
"""
NB sentiment analyser. 

Start code.
"""
import argparse
import pandas as pd

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
    
    """
    ADD YOUR CODE HERE
    Create functions and classes, using the best practices of Software Engineering
    """
    
    """
    training set -> estimate probabilities
    development set -> design the model
    test set -> evaluate generalisation power
    s∗ = argmax p(si) ∏ p(tj|si)
    """
    
    
    # read Phrases from file
    class Phrasesor:
        def __init__(self,phraseId,sentent,sentiment):
            self.phraseId = phraseId
            self.sentent = sentent
            self.sentiment = sentiment
        
        def phrases(filename):
            df = pd.read_csv(dev,index_col=0, delimiter="\t")
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
        
        
        def map5to3(self):
            for phrase in self.phrases:
                sentiment = phrase.sentiment
                if sentiment == 0 or sentiment == 1:
                    phrase.sentiment = 0
                elif sentiment == 2:
                    phrase.sentiment = 1
                elif sentiment == 3 or sentiment == 4:
                    phrase.sentiment = 2
            return self.phrases
    
    class BayesClassifer:
        
        def __init__(self, phrases):
            self.phrases = phrases
            self.classCountor()
            self.phraseClassifier()
            self.fearureCountor()
            self.likelihoodCalc()
            
            
            
        def classCountor(self):
            self.negCount=0
            self.neuCount=0
            self.posCount=0
            for phrase in self.phrases:
                sentiment = phrase.sentiment
                if sentiment == 0:
                    self.negCount+=1
                elif sentiment == 1:
                    self.neuCount+=1
                elif sentiment == 2:
                    self.posCount+=1
                else:
                    print("classCountor Error!")
            self.classCount = self.negCount + self.neuCount + self.posCount
            
            
        def phraseClassifier(self):
            self.posPhrase = []
            self.neuPhrase = []
            self.negPhrase = []
            for phrase in self.phrases:
                sentiment = phrase.sentiment
                if sentiment == 0:
                    self.posPhrase.append(phrase)
                elif sentiment == 1:
                    self.neuPhrase.append(phrase)
                elif sentiment == 2:
                    self.negPhrase.append(phrase)
                else:
                    print("phraseClassifier Error!")
                    
        def fearureCountor(self):
            self.posFeatureCount = 0
            self.posFeature = {}
            for phrase in self.posPhrase:
                for word in phrase.sentent:
                    if word in self.posFeature:
                        self.posFeature[word]+=1
                        self.posFeatureCount+=1
                    else:
                        self.posFeature[word]=1
                        self.posFeatureCount+=1
                        
            self.neuFeatureCount = 0
            self.neuFeature = {}
            for phrase in self.neuPhrase:
                for word in phrase.sentent:
                    if word in self.neuFeature:
                        self.neuFeature[word]+=1
                        self.neuFeatureCount+=1
                    else:
                        self.neuFeature[word]=1
                        self.neuFeatureCount+=1
                        
            
            self.negFeatureCount = 0
            self.negFeature = {}
            for phrase in self.negPhrase:
                for word in phrase.sentent:
                    if word in self.negFeature:
                        self.negFeature[word]+=1
                        self.negFeatureCount+=1
                    else:
                        self.negFeature[word]=1
                        self.negFeatureCount+=1

                
            
        
        def priorProbabilityCalc(self):
            self.negPrior = self.negCount / self.classCount
            self.neuPrior = self.neuCount / self.classCount
            self.posPrior = self.posCount / self.classCount
            return self.negPrior,self.neuPrior,self.posPrior
        
        def likelihoodCalc(self):
           self.posLikelihood = {}
           for feature in self.posFeature:
               self.posLikelihood[feature] = self.posFeature[feature] / self.posFeatureCount
               
           self.neuLikelihood = {}
           for feature in self.neuFeature:
                self.neuLikelihood[feature] = self.neuFeature[feature] / self.neuFeatureCount
                
           self.negLikelihood = {}
           for feature in self.negFeature:
                self.negLikelihood[feature] = self.negFeature[feature] / self.negFeatureCount
        
        def posteriorCalc(self):
            for phrase in self.phrases:
                print(phrase.phraseId)
          
            


            
    



    phrases = Phrasesor.phrases(training)
    processed = Processor(phrases).preProsess()
    to3Class = Processor(processed).map5to3()

    
    bayes = BayesClassifer(to3Class)
    negPrior,neuPrior,posPrior = bayes.priorProbabilityCalc()
    
    bayes.posteriorCalc()

    

    
        
          
            
            
    
    print()
    print('='*50,'Prior Probability','='*50)
    print("Negative Prior Probability: ",negPrior)
    print("Neutral Prior Probability: ",neuPrior)
    print("Positive Prior Probability: ",posPrior)
    #You need to change this in order to return your macro-F1 score for the dev set
    f1_score = 0
    

    """
    IMPORTANT: your code should return the lines below. 
    However, make sure you are also implementing a function to save the class predictions on dev and test sets as specified in the assignment handout
    """
    #print("Student\tNumber of classes\tFeatures\tmacro-F1(dev)\tAccuracy(dev)")
    print()
    print('='*50,'Evaluation','='*50)
    print("%s\t%d\t%s\t%f" % (USER_ID, number_classes, features, f1_score))

if __name__ == "__main__":
    main()