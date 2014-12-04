import nltk.classify.util
import os
import re

def dialogue_act_features(post):
    """Return a feature from an object of type nltk.util.LazySubsequence.

    Arguments:
    post -- object of type nltk.util.LazySubsequence

    Return values:
    Dictionary that represents a feature of a data set
    """
    features = {}
    # converts a post into an object that can be used later to train a nltk
    # classifier
    for word in nltk.word_tokenize(post):
        features['contains(%s)' % word.lower()] = True
    features['first_word'] = nltk.word_tokenize(post)[0].lower()
    return features


def dialogue_haveBe_features(question):
    features = {}
    features['first_word'] = nltk.word_tokenize(question)[0].lower()
    return features


def trainTypeQuestion():
    """Return a Naive Bayes Classifier.
    
    The classifier is trained with two traininf sets: an nltk set and another
    one with features that are parsed from a .txt file.

    Arguments:
    -

    Return values:
    Naive Bayes Classifier
    """
    # Retrieve information from the nltk chat package
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]

    # Training set to be add to the rest of the data set
    haveBeQuestions = ['Have you been here?', 'Are you okay?',
                       'Are you alive?', 'Am I a dragon?',
                       'Have you any idea?', 'Has she a cat?',
                       'Are we greedy?', 'Is he tired?', 'Is she good?',
                       'Are you sure?', 'Have you already done it?',
                       'Has he eaten it?', 'Is tomato red?']

    # Create data set
    featuresets = [(dialogue_act_features(post.text),
                    post.get('class'))for post in posts]

    # Extend data set with additional training set
    featuresets.extend([(dialogue_haveBe_features(q),
                         'ynQuestion') for q in haveBeQuestions])
    '''
    path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/firstClassifierAdditionalSentences.txt"
    path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/firstClassifierAdditionalSentences.txt"

    if os.path.exists(path1):
        filename = path1
    elif os.path.exists(path2):
        filename = path2
    else:
        print "Please insert the path to file firstClassifierAdditionalSentences.txt"
    '''
    # Extend data set with an additional training set from a txt file
    current_dir = os.getcwd()
    featuresets2 = labeledSentencesFileParser(current_dir + "/firstClassifierAdditionalSentences.txt")
    featuresets+=featuresets2

    train_set = featuresets
    # Train classifier
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier


def labeledSentencesFileParser(filename):
    """Return a set of features extracted from a .txt file.

    Arguments:
    filename -- name of .txt file to be parsed

    Return values:
    Set of features to be used to train a classifier.

    Restrictions:
    Txt file should have a specific syntax: question | questionLabel
    """
    # Open a file
    textFile = open(filename, "r")

    line = textFile.readlines()

    features = {}
    flag_label = 0
    every_words = []
    featureSets = []
    for l in line:
        sentence = [l.split()]
        for words in sentence:
            each_sentence = []
            for word in words:
                if word[0] == '#':
                    # This line is a comment
                    break
                if word == "|":
                    # Detected a question type label
                    flag_label = 1
                    continue
                if flag_label == 1:
                    # Retrieve question type label
                    label = re.findall(r"[\w']+|[.,!?;]", word)
                    flag_label = 0
                    continue
                each_word = re.findall(r"[\w']+|[.,!?;:]", word)
                every_words += each_word
                # Each word of the sentence is added 
                each_sentence += each_word
            if each_sentence:
                features = {}
                featureSet = ()
                # Each sentence is converted to the right syntax, in order to
                # train the classifier
                for word_ in each_sentence:
                    features['contains(%s)' % word_.lower()] = True
                featureSet = (features, label[0])
                # Add sentence feature to the data set
                featureSets.append(featureSet)
    # Close opened file
    textFile.close()
    return featureSets


def trainWhQuestion(mode):
    """Return a classifier trained with one of the training sets.

    Arguments:
    mode -- takes value 1 if classifier is trained to classify whQuestions
            takes value 2 if classifier is trained to classify DescriptionOther
            takes value 3 if classifier is trained to classify DescriptionH
            takes value 4 if classifier is trained to classify DescriptionWh

    Return values:
    Naive Bayes Classifier
    """

    current_dir = os.getcwd()
    # Choose mode to train different classifiers. Each mode corresponds to a
    # specific classifier
    if(mode == 1):
        filename = current_dir + "/whQuestionClassifiedSentences.txt"
        '''
        path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/whQuestionClassifiedSentences.txt"
        path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/whQuestionClassifiedSentences.txt"
        '''
    elif(mode == 2):
        filename = current_dir + "/classifierDescriptionOther.txt"
        '''
        path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/classifierDescriptionOther.txt"
        path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/classifierDescriptionOther.txt"
        '''
    elif(mode == 3):
        filename = current_dir + "/classifierDescriptionH.txt"
        '''
        path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/classifierDescriptionH.txt"
        path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/classifierDescriptionH.txt"
        '''
    elif(mode == 4):
        filename = current_dir + "/classifierDescriptionWh.txt"
        '''
        path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/classifierDescriptionWh.txt"
        path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/classifierDescriptionWh.txt"
        '''
        
    '''
    if os.path.exists(path1):
        file = path1
    else:
        file = path2
    '''
    featuresets = labeledSentencesFileParser(filename)

    train_set = featuresets
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier


def getPosNegWords():
    current_dir = os.getcwd()
    '''
    path1 = "/home/jens/Documents/DTU/Data Mining Using Python/Project/turbot/learn/SentiWordNet_3.0.0_20130122.txt"
    path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/SentiWordNet_3.0.0_20130122.txt"
    path3 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/SentiWordNet_3.0.0_20130122.txt"

    if os.path.exists(path1):
        file = path1
    elif os.path.exists(path2):
        file = path2
    else:
        file = path3
    '''
    words = dict()
    with open(current_dir + "/SentiWordNet_3.0.0_20130122.txt", 'r') as f:
        lines = f.readlines()[1:-1]
        for line in lines:
            columns = line.split('\t')
            word = columns[4].split('#')[0]
            words[word] = float(columns[2]) - float(columns[3])

    return words
