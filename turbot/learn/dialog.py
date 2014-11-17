import nltk.classify.util


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
                       'Has he eaten it?']

    featuresets = [(dialogue_act_features(post.text),
                    post.get('class'))for post in posts]

    featuresets.extend([(dialogue_haveBe_features(q),
                         'ynQuestion') for q in haveBeQuestions])

    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
    return nltk.NaiveBayesClassifier.train(train_set)


def getPosNegWords():
    file = "/home/jens/Documents/DTU/Data Mining Using Python/Project/turbot/learn/SentiWordNet_3.0.0_20130122.txt"
    words = dict()
    with open(file, 'r') as f:
        lines = f.readlines()[1:-1]
        for line in lines:
            columns = line.split('\t')
            word = columns[4].split('#')[0]
            words[word] = float(columns[2]) - float(columns[3])

    return words
