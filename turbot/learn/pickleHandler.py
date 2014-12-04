# -*- coding: utf-8 -*-

"""Module that handles pickle objects.

Functions:
save_object -- save a pickle object
load_object -- load an object from a pickle file
update_classifiers -- train a classifier and save it as pickle object
"""

import cPickle as pickle
import os
import dialog
import markov


def save_object(obj, filename):
    """Save pickle object with specified name.

    Arguments:
    obj -- object to be saved into a pickle file
    filename -- desired name of the pickle file to be saved

    Return values:
    -
    """
    '''
    path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/"
    "Repository/turbot/learn/"
    path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/"
    path3 = "/home/jens/Documents/DTU/Data Mining Using Python/Project/turbot/"
    "learn/"

    if os.path.exists(path1):
        filename = path1 + filename
    elif os.path.exists(path2):
        filename = path2 + filename
    elif os.path.exists(path3):
        filename = path3 + filename
    else:
        print "Please insert the path to the folder the where object will be "
        "saved."
    '''
    current_dir = os.getcwd()
    with open(current_dir + filename, 'wb') as output:
        pickle.dump(obj, output)


def load_object(filename):
    """Load pickle file.

    Arguments:
    filename -- name of the pickle file to be loaded

    Return values:
    pickle object
    """
    current_dir = os.getcwd()
    '''
    path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/"
    "Repository/turbot/learn/"
    path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/"
    path3 = "/home/jens/Documents/DTU/Data Mining Using Python/Project/turbot/"
    "learn/"

    if os.path.exists(path1):
        path = path1 + filename
    elif os.path.exists(path2):
        path = path2 + filename
    elif os.path.exists(path3):
        path = path3 + filename
    else:
        print "Please insert the path to the folder the where "
        "object will be loaded from."
    '''
    with open(current_dir + filename, 'rb') as input:
        return pickle.load(input)


def update_classifiers():
    """Train and save classifier pickle files.

    Arguments:
    -

    Return values:
    -
    """
    trainTypeQClassifier = dialog.trainTypeQuestion()
    trainWhQuestionClassifier = dialog.trainWhQuestion(1)
    trainDescOtherQuestionClassifier = dialog.trainWhQuestion(2)
    trainDescHQuestionClassifier = dialog.trainWhQuestion(3)
    trainDescWhQuestionClassifier = dialog.trainWhQuestion(4)
    trainSentencesMarkov = markov.Markov()

    # Save classifier that determines the general type of question
    save_object(trainTypeQClassifier, 'classifierTypeQ.pkl')
    # Save classifier that determines the type of "WhQuestion"
    save_object(trainWhQuestionClassifier, 'classifierWhQ.pkl')
    # Save classifier that determines the type of "DescriptionOther"
    save_object(trainDescOtherQuestionClassifier, 'classifierDescOtherQ.pkl')
    # Save classifier that determines the type of "DescriptionH"
    save_object(trainDescHQuestionClassifier, 'classifierDescHQ.pkl')
    # Save classifier that determines the type of "DescriptionWh"
    save_object(trainDescWhQuestionClassifier, 'classifierDescWhQ.pkl')
    # Save markov chains from sentenes dataset
    save_object(trainSentencesMarkov.getMarkov(), 'markovSentences.pkl')

# TODO delete these lines
# Call function update_classifiers to update the classifier files
#update_classifiers()
