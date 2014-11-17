import nltk.classify.util
import re







def labeledSentencesFileParser(filename):

    # Open a file
    textFile = open(filename, "r")
    #print "Name of the file: ", textFile.name
    
    line = textFile.readlines()
#    print "Read Line: %s" % (line)
    
    features = {}
    flag_label=0
    every_words=[]
    featureSets=[]
    for l in line:
        sentence=[l.split()]
        for words in sentence:
            each_sentence=[]
            for word in words:
                if word[0] == '#':
#                    print "This line is a comment"
                    break
                if word == "|":
                    flag_label=1
                    continue
                if flag_label==1:
                    label = re.findall(r"[\w']+|[.,!?;]", word)
                    flag_label=0
                    continue
                each_word=re.findall(r"[\w']+|[.,!?;:]", word)
                every_words+=each_word
                each_sentence+=each_word
            if each_sentence:
                features={}
                featureSet=()
                for word_ in each_sentence:
                    features['contains(%s)' % word_.lower()] = True
                featureSet=(features,label[0])
                featureSets.append(featureSet)
    # Close opend file
    textFile.close()
    #print featureSets
    return featureSets









posts = nltk.corpus.nps_chat.xml_posts()[:10000]


def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
#        print word
        features['contains(%s)' % word.lower()] = True
    return features

featuresets = [(dialogue_act_features(post.text),
                post.get('class'))for post in posts]


featuresets2 = labeledSentencesFileParser("ClassifiedSentences.txt")
#print featuresets2[:20]
#print "------------------\n----------------\n------"
featuresets+=featuresets2
print featuresets[:20]

size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
#print(nltk.classify.accuracy(classifier, test_set))

while True:
    print classifier.classify(
        dialogue_act_features(raw_input('Enter your input:')))
