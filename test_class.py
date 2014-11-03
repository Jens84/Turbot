import nltk.classify.util


posts = nltk.corpus.nps_chat.xml_posts()[:40000]


def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains(%s)' % word.lower()] = True
    return features

featuresets = [(dialogue_act_features(post.text),
                post.get('class'))for post in posts]

size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))

while True:
    print classifier.classify(
        dialogue_act_features(raw_input('Enter your input:')))