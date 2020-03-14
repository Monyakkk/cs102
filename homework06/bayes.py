import string
from math import log


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


class NaiveBayesClassifier:

    def __init__(self):
        self.allwords = []
        self.column = {}   #word, labels, sum, chances
        self.words_counter = 0
        self.labels_counter = {}
        self.PPOS = 0
        self.PNEU = 0
        self.PNEG = 0   #Apriore chances
        

    def fit(self, X, y): #X=string title, y=string label
        """ Fit Naive Bayes classifier according to X, y. """
        
        for _ in range (len(X)):   #Going through news
            
            label = y[_]
            title_words = clean(X[_]).lower().split() #=array of words in title
                     
            try:
                self.labels_counter[label] += 1
            except KeyError:
                self.labels_counter[label] = 1
                           
            for i in range (len(title_words)):    #Going through words in news title, title_words[i]=current word
                self.words_counter += 1
                for j in range(len(self.allwords)):
                    if self.allwords[j]['word'] == title_words[i]:
                        try:
                            self.allwords[j][label] += 1
                        except KeyError:
                            self.allwords[j][label] = 1  
                        break
                else:
                    self.allwords.append({})
                    self.allwords[len(self.allwords)-1]['good'] = 0
                    self.allwords[len(self.allwords)-1]['maybe'] = 0
                    self.allwords[len(self.allwords)-1]['never'] = 0
                    self.allwords[len(self.allwords)-1]['word'] = title_words[i]
                    self.allwords[len(self.allwords)-1][label] = 1
                    break
            
        for t in range (len(self.allwords)):
            self.allwords[t]['sum'] = self.allwords[t]['good'] + self.allwords[t]['maybe'] + self.allwords[t]['never']
            self.allwords[t]['PwiPOS'] = (self.allwords[t]['good'] + 1)/(self.allwords[t]['sum'] + self.words_counter)
            self.allwords[t]['PwiNEU'] = (self.allwords[t]['maybe'] + 1)/(self.allwords[t]['sum'] + self.words_counter)
            self.allwords[t]['PwiNEG'] = (self.allwords[t]['never'] + 1)/(self.allwords[t]['sum'] + self.words_counter)
        self.PPOS = self.labels_counter['good']/len(X)
        self.PNEU = self.labels_counter['maybe']/len(X)
        self.PNEG = self.labels_counter['never']/len(X) #Apriore chances

                
    def predict(self, X):   #X=list of titles
        """ Perform classification on an array of test vectors X. """
        labels_predicted = []
        for titles in X:
            words_list = clean(titles).lower().split()
            good_chance = log(self.PPOS)
            maybe_chance =log(self.PNEU)
            never_chance = log(self.PNEG)
            for words in words_list:
                for i in range (len(self.allwords)):
                    if self.allwords[i]['word'] == words:
                        good_chance += log(self.allwords[i]['PwiPOS'])
                        maybe_chance += log(self.allwords[i]['PwiNEU'])
                        never_chance += log(self.allwords[i]['PwiNEG'])
                        break
                    
            if good_chance > maybe_chance and good_chance > never_chance:
                labels_predicted.append('good')
            if maybe_chance > good_chance and maybe_chance > never_chance:
                labels_predicted.append('maybe')
            if never_chance > maybe_chance and never_chance > good_chance:
                labels_predicted.append('never')
       
        return labels_predicted    

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        predicted = self.predict(X_test)
        right_labels = 0
        for predicted_label, label in zip(predicted, y_test):
            if predicted_label == label:
                right_labels += 1
        result = right_labels / len(X_test)
        return result






    

