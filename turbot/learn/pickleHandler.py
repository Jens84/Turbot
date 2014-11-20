# -*- coding: utf-8 -*-

#import cPickle as pickle
import pickle
import os
import dialog

def save_object(obj, filename):

    path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/"
    path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/"
    path3 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/"


    if os.path.exists(path1):
        filename = path1 + filename
    elif os.path.exists(path2):
        filename = path2 + filename
    elif os.path.exists(path3):
        filename = path3 + filename
    else:
        print "Please insert the path to the folder the where object will be saved."
    
    with open(filename, 'wb') as output:
        pickle.dump(obj, output)


def load_object(filename):
  

    path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/"
    path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/"
    path3 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/"


    if os.path.exists(path1):
        path = path1 + filename
    elif os.path.exists(path2):
        path = path2 + filename
    elif os.path.exists(path3):
        path = path3 + filename
    else:
        print "Please insert the path to the folder the where object will be loaded from."
    
    with open(path, 'rb') as input:
        return pickle.load(input)




def update_classifiers():
    
    trainWhQuestionClassifier = dialog.trainWhQuestion()
    trainTypeQClassifier = dialog.trainTypeQuestion()

    save_object(trainWhQuestionClassifier, 'classifierWhQ.pkl')
    save_object(trainTypeQClassifier, 'classifierTypeQ.pkl')



update_classifiers()

