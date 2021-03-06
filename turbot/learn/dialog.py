""" Script for sentence classifier generation.

Functions:
dialogue_act_features
dialogue_haveBe_features
trainTypeQuestion
labeledSentencesFileParser
trainWhQuestion
getPosNegWords
"""

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
    """ Create a feature from a question.

    Arguments:
    question -- string with a question
    """
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
    # Extend data set with an additional training set from a txt file
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    featuresets2 = labeledSentencesFileParser(
        os.path.join(__location__, "firstClassifierAdditionalSentences.txt"))
    featuresets += featuresets2

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
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    # Choose mode to train different classifiers. Each mode corresponds to a
    # specific classifier
    if(mode == 1):
        filename = os.path.join(__location__,
                                "whQuestionClassifiedSentences.txt")
    elif(mode == 2):
        filename = os.path.join(__location__,
                                "classifierDescriptionOther.txt")
    elif(mode == 3):
        filename = os.path.join(__location__,
                                "classifierDescriptionH.txt")
    elif(mode == 4):
        filename = os.path.join(__location__,
                                "classifierDescriptionWh.txt")

    featuresets = labeledSentencesFileParser(filename)

    train_set = featuresets

    # Train classifier
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier


def getPosNegWords():
    """Return a dictionary with each word and his happiness score.

    Arguments:
    -

    Return values:
    dictionary of words
    """
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    filename = os.path.join(__location__,
                            "SentiWordNet_3.0.0_20130122.txt")

    words = dict()
    with open(filename, 'r') as f:
        lines = f.readlines()[1:-1]
        for line in lines:
            columns = line.split('\t')
            word = columns[4].split('#')[0]
            words[word] = float(columns[2]) - float(columns[3])

    return words
