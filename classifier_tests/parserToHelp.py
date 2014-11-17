# -*- coding: utf-8 -*-
"""
Created on Mon Nov 17 16:50:30 2014

@author: joseesteves
"""


def fileParserToHelp(filename):

    # Open a file
    textFile = open(filename, "r")
    print "Name of the file: ", textFile.name
    
    line = textFile.readlines()
#    print "Read Line: %s" % (line)
    for l in line:
        beggining = l.split(':')[0]
        if beggining == "HUM":
            print ' '.join([word for word in l.split(' ')[1:]])[:-1],"| Entity"
    # Close opend file
    textFile.close()
    return

fileParserToHelp('randomTrainSet.txt')


