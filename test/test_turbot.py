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

'''
def test_trainWhQuestion1():
    d = turbot.Dialog()
    assert(d.("When was the ww2?")
           == "This question is of type wh and its category is: Time")
    assert(d.answer("When was the the world trade center bombed?")
           == "This question is of type wh and its category is: Time")
    assert(d.answer("Where is Wally?")
           == "This question is of type wh and its category is: Place")
    assert(d.answer("Where was the first concert of U2?")
           == "This question is of type wh and its category is: Place")


def test_trainWhQuestion2():
    d = turbot.Dialog()
    assert(d.answer("Who was the first singer of the Abba band?")
           == "This question is of type wh and its category is: Entity")
    assert(d.answer("Who was the first king of spain?")
           == "This question is of type wh and its category is: Entity")
    assert(d.answer("Why did my girlfriend leave me?")
           == "This question is of type wh and its category is: Reason")
    assert(d.answer("Why am I sad?")
           == "This question is of type wh and its category is: Reason")


def test_trainWhQuestion3():
    d = turbot.Dialog()
    assert(d.answer("How do you go to the Zoo?")
           == "This question is of type wh and its category is: Manner")
    assert(d.answer("How should I go from the Arctic to Greenland?")
           == "This question is of type wh and its category is: Manner")
    assert(d.answer("What are cars made of?")
           == "This question is of type wh and its category is: DescriptionWh")
    assert(d.answer("What is the paint of my bag made of?")
           == "This question is of type wh and its category is: DescriptionWh")


def test_trainWhQuestion4():
    d = turbot.Dialog()
    assert(d.answer("What does selfish mean?")
           == "This question is of type wh and its category is: DescriptionWh")
    assert(d.answer("What is the meaning of toothbrush?")
           == "This question is of type wh and its category is: DescriptionWh")
    assert(d.answer("What does I.S.N. stand for?")
           == "This question is of type wh and its category is: DescriptionWh")
    assert(d.answer(
           """How old do I have to be to get a
           driver's license in the Portugal?""")
           == "This question is of type wh and its category is: DescriptionH")


def test_trainWhQuestion5():
    d = turbot.Dialog()
    assert(d.answer("How much hair does an ordinary bear have?")
           == "This question is of type wh and its category is: DescriptionH")
    assert(d.answer("What does a jew look like?")
           == """This question is of type wh and its category
                 is: DescriptionOther""")
    assert(d.answer("What is a dragon like?")
           == """This question is of type wh and its category
                 is: DescriptionOther""")
    assert(d.answer("What is the form of a chain?")
           == """"This question is of type wh and its category
                  is: DescriptionOther""")
'''
