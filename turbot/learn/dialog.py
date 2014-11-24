import nltk.classify.util
import os
import re


def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains(%s)' % word.lower()] = True
    features['first_word'] = nltk.word_tokenize(post)[0].lower()
    return features


def dialogue_haveBe_features(question):
    features = {}
    features['first_word'] = nltk.word_tokenize(question)[0].lower()
    return features


def trainTypeQuestion():
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]

    haveBeQuestions = ['Have you been here?', 'Are you okay?',
                       'Are you alive?', 'Am I a dragon?',
                       'Have you any idea?', 'Has she a cat?',
                       'Are we greedy?', 'Is he tired?', 'Is she good?',
                       'Are you sure?', 'Have you already done it?',
                       'Has he eaten it?', 'Is tomato red?']

    featuresets = [(dialogue_act_features(post.text),
                    post.get('class'))for post in posts]

    featuresets.extend([(dialogue_haveBe_features(q),
                         'ynQuestion') for q in haveBeQuestions])
    path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/firstClassifierAdditionalSentences.txt"
    path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/firstClassifierAdditionalSentences.txt"

    if os.path.exists(path1):
        filename = path1
    elif os.path.exists(path2):
        filename = path2
    else:
        print "Please insert the path to file firstClassifierAdditionalSentences.txt"
    
    featuresets2 = labeledSentencesFileParser(filename)
    featuresets+=featuresets2

    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    return nltk.NaiveBayesClassifier.train(train_set)


def labeledSentencesFileParser(filename):

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
#                    print "This line is a comment"
                    break
                if word == "|":
                    flag_label = 1
                    continue
                if flag_label == 1:
                    label = re.findall(r"[\w']+|[.,!?;]", word)
                    flag_label = 0
                    continue
                each_word = re.findall(r"[\w']+|[.,!?;:]", word)
                every_words += each_word
                each_sentence += each_word
            if each_sentence:
                features = {}
                featureSet = ()
                for word_ in each_sentence:
                    features['contains(%s)' % word_.lower()] = True
                featureSet = (features, label[0])
                featureSets.append(featureSet)
    # Close opend file
    textFile.close()
    return featureSets


def trainWhQuestion(mode):
    
    # Choose mode to train different classifiers
    if(mode == 1):
        path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/whQuestionClassifiedSentences.txt"
        path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/whQuestionClassifiedSentences.txt"
    elif(mode == 2):
        path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/classifierDescriptionOther.txt"
        path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/classifierDescriptionOther.txt"
    elif(mode == 3):
        path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/classifierDescriptionH.txt"
        path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/classifierDescriptionH.txt"
    elif(mode == 4):
        path1 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/classifierDescriptionWh.txt"
        path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/classifierDescriptionWh.txt"
        
    if os.path.exists(path1):
        file = path1
    else:
        file = path2

    featuresets = labeledSentencesFileParser(file)

    size = int(len(featuresets) * 0.05)
    train_set, test_set = featuresets[size:], featuresets[:size]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    return classifier


def getPosNegWords():
    path1 = "/home/jens/Documents/DTU/Data Mining Using Python/Project/turbot/learn/SentiWordNet_3.0.0_20130122.txt"
    path2 = "/home/beljul/DTU/Data mining using Python/Project/turbot/learn/SentiWordNet_3.0.0_20130122.txt"
    path3 = "/Users/joseesteves/Documents/Erasmus/DTU/Data Mining/Git/Repository/turbot/learn/SentiWordNet_3.0.0_20130122.txt"

    if os.path.exists(path1):
        file = path1
    elif os.path.exists(path2):
        file = path2
    else:
        file = path3

    words = dict()
    with open(file, 'r') as f:
        lines = f.readlines()[1:-1]
        for line in lines:
            columns = line.split('\t')
            word = columns[4].split('#')[0]
            words[word] = float(columns[2]) - float(columns[3])

    return words
