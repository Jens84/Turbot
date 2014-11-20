# -*- coding: utf-8 -*-

#import cPickle as pickle
import pickle
import os
import dialog

def save_object(obj, filename):

    path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/"

    if os.path.exists(path1):
        filename = path1 + filename
    else:
        print "Please insert the path to the folder the where object will be saved."
    
    with open(filename, 'wb') as output:
        pickle.dump(obj, output)
#        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def load_object(filename):
    
    path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/"

    if os.path.exists(path1):
        path = path1 + filename
    else:
        print "Please insert the path to the folder the where object will be saved."
    
#    path = path + filename
    
    with open(path, 'rb') as input:
        return pickle.load(input)




def update_classifiers():
    
    trainWhQuestionClassifier = dialog.trainWhQuestion()
    trainTypeQClassifier = dialog.trainTypeQuestion()

    save_object(trainWhQuestionClassifier, 'classifierWhQ.pkl')
    save_object(trainTypeQClassifier, 'classifierTypeQ.pkl')



update_classifiers()

