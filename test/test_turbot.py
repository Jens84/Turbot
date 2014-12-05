import turbot


def test_YesNo_basic():
    d = turbot.Dialog()
    assert(d.answer("Are you okay?") == "Yes, I am okay.")
    assert(d.answer("Are you sure?") == "No, I am not sure.")
    assert(d.answer("Has he a brother?") == "Yes, he has a brother.")
    assert(d.answer("Do you know him?") == "Yes, I know him.")
    assert(d.answer("Are they fine?") == "Yes, they are fine.")


def test_YesNo_complex():
    d = turbot.Dialog()
    assert(d.answer("Is Barack Obama the president?")
           == "Yes, Barack Obama is the president.")
    assert(d.answer("Do you know Francois Hollande?")
           == "Yes, I know Francois Hollande.")
    assert(d.answer("Have you been at school?")
           == "No, I have not been at school.")
    assert(d.answer("Has he a brother?") == "Yes, he has a brother.")


def test_YesNo_tenses():
    d = turbot.Dialog()
    assert(d.answer("Have you been at school?")
           == "No, I have not been at school.")
    assert(d.answer("Will you see the movie?") == "Yes, I will see the movie.")
    assert(d.answer("Did you play tennis") == "Yes, I played tennis.")


def test_YesNo_wikipedia():
    d = turbot.Dialog()
    assert(d.answer("Is Merkel a singer?") == "No, Merkel is not a singer.")
    assert(d.answer("Is Obama the president?")
           == "Yes, Obama is the president.")
    assert(d.answer("Is Paris in France?") == "Yes, Paris is in France.")
    assert(d.answer("Is London in United Kingdom?")
           == "Yes, London is in United Kingdom.")


def test_whYesNo_wikipedia():
    d = turbot.Dialog()
    assert(d.answer("Is Merkel a singer?") == "No, Merkel is not a singer.")
    assert(d.answer("Is Obama the president?")
           == "Yes, Obama is the president.")
    assert(d.answer("Is Paris in France?") == "Yes, Paris is in France.")
    assert(d.answer("Is London in United Kingdom?")
           == "Yes, London is in United Kingdom.")


def test_trainWhQuestion1():
    classifier = turbot.learn.pickleHandler.load_object('classifierWhQ.pkl')
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features("When was the ww2?"))
        == "TimeWhen")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "When was the the world trade center bombed?")) == "TimeWhen")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "In what day was Justin Bieber born?")) == "TimeWhat")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "Where is Wally?")) == "Place")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "Where was James Bond born?")) == "Place")


def test_trainWhQuestion2():
    classifier = turbot.learn.pickleHandler.load_object('classifierWhQ.pkl')
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "Who was the first singer of the Abba band?")) == "Entity")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "Who is the king of spain?")) == "Entity")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "Why did my girlfriend leave me?")) == "Reason")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "Why am I sad?")) == "Reason")


def test_trainWhQuestion3():
    classifier = turbot.learn.pickleHandler.load_object('classifierWhQ.pkl')
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "How do you go to the Zoo?")) == "Manner")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "How should I go from the Arctic to Greenland?")) == "Manner")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "What are helicopters made of?")) == "DescriptionWh")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "What is the paint of my bag made of?")) == "DescriptionWh")


def test_trainWhQuestion4():
    classifier = turbot.learn.pickleHandler.load_object('classifierWhQ.pkl')
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "What does selfish mean?")) == "DescriptionWh")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "What is the meaning of toothbrush?")) == "DescriptionWh")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "What does I.S.N. stand for?")) == "DescriptionWh")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "How old is Bjorn?")) == "DescriptionH")


def test_trainWhQuestion5():
    classifier = turbot.learn.pickleHandler.load_object('classifierWhQ.pkl')
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "How much hair does an ordinary bear have?"))
           == "DescriptionH")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "What does a jew look like?")) == "DescriptionOther")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "What is a dragon like?")) == "DescriptionOther")
    assert(classifier.classify(
        turbot.learn.dialog.dialogue_act_features(
            "What is the form of a chain?")) == "DescriptionOther")
