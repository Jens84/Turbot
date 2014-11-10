import nltk.classify.util


def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains(%s)' % word.lower()] = True
    return features


def trainTypeQuestion():
    posts = nltk.corpus.nps_chat.xml_posts()[:10000]
    featuresets = [(dialogue_act_features(post.text),
                    post.get('class'))for post in posts]

    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    return nltk.NaiveBayesClassifier.train(train_set)
