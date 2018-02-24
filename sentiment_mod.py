from nltk.classify.scikitlearn import SklearnClassifier
import pickle, random, nltk

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
            try:
               mod=mode(votes)
            except:
               mod=max(set(votes),key=votes.count)
        return mod

    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf



documents_f = open("pickled_algos/documents.pickle","rb")
documents = pickle.load(documents_f)
documents_f.close()

features_f = open("pickled_algos/word_features5k.pickle","rb")
word_features = pickle.load(features_f)
features_f.close()

def find_features(document): 
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)

    return features

load_documents = open("pickled_algos/featuresets.pickle","rb")
featuresets = pickle.load(load_documents)
load_documents.close()

random.shuffle(featuresets)
   
training_set = featuresets[:5500]
testing_set =  featuresets[5500:]


load_classifier = open("pickled_algos/default_classifier.pickle","rb")
default_classifier = pickle.load(load_classifier)
load_classifier.close()
##default_classifier = nltk.NaiveBayesClassifier.train(training_set)
##print("Original Naive Bayes Algo accuracy percent:", (nltk.classify.accuracy(default_classifier, testing_set))*100)
##default_classifier.show_most_informative_features(15)
##save_classifier = open("pickled_algos/default_classifier.pickle","wb")
##pickle.dump(default_classifier, save_classifier)
##save_classifier.close()

load_classifier = open("pickled_algos/MNB_classifier.pickle","rb")
MNB_classifier = pickle.load(load_classifier)
load_classifier.close()

load_classifier = open("pickled_algos/BernoulliNB_classifier.pickle","rb")
BernoulliNB_classifier = pickle.load(load_classifier)
load_classifier.close()

load_classifier = open("pickled_algos/LogisticRegression_classifier.pickle","rb")
LogisticRegression_classifier = pickle.load(load_classifier)
load_classifier.close()

load_classifier = open("pickled_algos/SGDClassifier_classifier.pickle","rb")
SGDClassifier_classifier = pickle.load(load_classifier)
load_classifier.close()

load_classifier = open("pickled_algos/LinearSVC_classifier.pickle","rb")
LinearSVC_classifier = pickle.load(load_classifier)
load_classifier.close()

load_classifier = open("pickled_algos/NuSVC_classifier.pickle","rb")
NuSVC_classifier = pickle.load(load_classifier)
load_classifier.close()

voted_classifier = VoteClassifier(default_classifier,
                                  NuSVC_classifier,
                                  LinearSVC_classifier,
                                  SGDClassifier_classifier,
                                  MNB_classifier,
                                  BernoulliNB_classifier,
                                  LogisticRegression_classifier)

def sentiment(text):
    feats = find_features(text)
    return voted_classifier.classify(feats),voted_classifier.confidence(feats)
