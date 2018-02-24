import nltk, sqlite3
import random
from nltk.corpus import movie_reviews
from nltk.classify.scikitlearn import SklearnClassifier
import pickle

from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from nltk.classify import ClassifierI
from statistics import mode

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords



class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

    
tags =              ['russia', 'russian','russians','moscow', 'soviet',          
                    'kremlin','saint petersburg', 'stalin', 'communists',
                    'ussr','soviet','putin','navalny', 'chechnya',
                    'ukraine','ukranian','ukranians']

#tags +=[',','.','!',"'s","'",'the','a',"n't",'--', '?',     '(',')']


conn = sqlite3.connect('comments.db')
c = conn.cursor()

def read_from_db():
    c.execute('SELECT * FROM stuffToPlot')
    
    for row in c.fetchall():
        print(row)
    
        


documents = []


allowed_word_types = ["J", "R", "V", "NN", "RB", "JJ", "VBP","VB","VBD"]

all_words = []

c.execute('SELECT * FROM pos_comms')
for r,pol in c.fetchall():
##    print(r, pol)
    documents.append( (r, "pos") )
    words = word_tokenize(r)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())
            
c.execute('SELECT * FROM neg_comms')
for r, pol in c.fetchall():
    documents.append( (r, "neg") )
    words = word_tokenize(r)
    pos = nltk.pos_tag(words)
    for w in pos:
        if w[1][0] in allowed_word_types:
            all_words.append(w[0].lower())


save_documents = open("pickled_algos/documents.pickle","wb")
pickle.dump(documents, save_documents)
save_documents.close()

all_words = nltk.FreqDist(all_words)

stop_words = set(stopwords.words("english"))
for w in tags:
	stop_words.add(w)

word_features = [w[0] for w in all_words.most_common(3000)]                           #генерирует список самых часто встречающихся слов
filtered_word_features = [word for word in word_features if not word in stop_words]   #убирает не значащие слова

save_features = open("pickled_algos/word_features5k.pickle","wb")
pickle.dump(filtered_word_features, save_features)
save_features.close()

def find_features(document): 
    words = word_tokenize(document)
    features = {}
    for w in filtered_word_features:
        features[w] = (w in words)

    return features         #возвращает dictionary с ключами - словами(str) и соответствующими им True or False, указывающими есть ли в документе это слово или нет



featuresets = [(find_features(rev), category) for (rev, category) in documents] 

random.shuffle(featuresets)
   
training_set = featuresets[:5500]
testing_set =  featuresets[5500:]

##5
### negative data example:      
##training_set = featuresets[100:]
##testing_set =  featuresets[:100]


default_classifier = nltk.NaiveBayesClassifier.train(training_set)
print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(default_classifier, testing_set))*100)
default_classifier.show_most_informative_features(15)
save_classifier = open("pickled_algos/default_classifier.pickle","wb")
pickle.dump(default_classifier, save_classifier)
save_classifier.close()

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set))*100)
save_classifier = open("pickled_algos/MNB_classifier.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
BernoulliNB_classifier.train(training_set)
print("BernoulliNB_classifier accuracy percent:", (nltk.classify.accuracy(BernoulliNB_classifier, testing_set))*100)
save_classifier = open("pickled_algos/BernoulliNB_classifier.pickle","wb")
pickle.dump(BernoulliNB_classifier, save_classifier)
save_classifier.close()

LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
LogisticRegression_classifier.train(training_set)
print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)
save_classifier = open("pickled_algos/LogisticRegression_classifier.pickle","wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)
save_classifier = open("pickled_algos/SGDClassifier_classifier.pickle","wb")
pickle.dump(SGDClassifier_classifier, save_classifier)
save_classifier.close()

##SVC_classifier = SklearnClassifier(SVC())
##SVC_classifier.train(training_set)
##print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)
##save_classifier = open("pickled_algos/SVC_classifier.pickle","wb")
##pickle.dump(SVC_classifier, save_classifier)
##save_classifier.close()

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)
save_classifier = open("pickled_algos/LinearSVC_classifier.pickle","wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)
save_classifier = open("pickled_algos/NuSVC_classifier.pickle","wb")
pickle.dump(NuSVC_classifier, save_classifier)
save_classifier.close()


voted_classifier = VoteClassifier(default_classifier,
                                  NuSVC_classifier,
                                  LinearSVC_classifier,
                                  SGDClassifier_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

print("voted_classifier accuracy percent:", (nltk.classify.accuracy(voted_classifier, testing_set))*100)

c.close()
conn.close()


