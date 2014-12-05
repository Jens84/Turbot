import turbot
import unittest
import pytest


class TurbotTest(unittest.TestCase):
    _d = None
    _classifierType = None
    _classifierWh = None
    _classifierDescriptionWh = None
    _classifierDescriptionH = None
    _classifierDescriptionOther = None

    @pytest.fixture(autouse=True)
    def init(self):
        self._d = turbot.Dialog()
        self._classifierType = (turbot.learn.pickleHandler.
                                load_object('classifierTypeQ.pkl'))
        self._classifierWh = (turbot.learn.pickleHandler.
                              load_object('classifierWhQ.pkl'))
        self._classifierDescriptionWh = (turbot.learn.pickleHandler.
                                         load_object('classifierDescWhQ.pkl'))
        self._classifierDescriptionH = (turbot.learn.pickleHandler.
                                        load_object('classifierDescHQ.pkl'))
        self._classifierDescriptionOther = (turbot.learn.pickleHandler.
                                            load_object(
                                                'classifierDescOtherQ.pkl'))

    def test_YesNo_basic(self):
        assert(self._d.answer("Are you okay?") == "Yes, I am okay.")
        assert(self._d.answer("Are you sure?") == "No, I am not sure.")
        assert(self._d.answer("Has he a brother?") == "Yes, he has a brother.")
        assert(self._d.answer("Do you know him?") == "Yes, I know him.")
        assert(self._d.answer("Are they fine?") == "Yes, they are fine.")

    def test_YesNo_complex(self):
        assert(self._d.answer("Is Barack Obama the president?")
               == "Yes, Barack Obama is the president.")
        assert(self._d.answer("Do you know Francois Hollande?")
               == "Yes, I know Francois Hollande.")
        assert(self._d.answer("Have you been at school?")
               == "No, I have not been at school.")
        assert(self._d.answer("Has he a brother?") == "Yes, he has a brother.")

    def test_YesNo_tenses(self):
        assert(self._d.answer("Have you been at school?")
               == "No, I have not been at school.")
        assert(self._d.answer("Will you see the movie?")
               == "Yes, I will see the movie.")
        assert(self._d.answer("Did you play tennis")
               == "Yes, I played tennis.")

    def test_YesNo_wikipedia(self):
        assert(self._d.answer("Is Merkel a singer?")
               == "No, Merkel is not a singer.")
        assert(self._d.answer("Is Obama the president?")
               == "Yes, Obama is the president.")
        assert(self._d.answer("Is Paris in France?")
               == "Yes, Paris is in France.")
        assert(self._d.answer("Is London in United Kingdom?")
               == "Yes, London is in United Kingdom.")

    def test_whYesNo_wikipedia(self):
        assert(self._d.answer("Is Merkel a singer?")
               == "No, Merkel is not a singer.")
        assert(self._d.answer("Is Obama the president?")
               == "Yes, Obama is the president.")
        assert(self._d.answer("Is Paris in France?")
               == "Yes, Paris is in France.")
        assert(self._d.answer("Is London in United Kingdom?")
               == "Yes, London is in United Kingdom.")

    def test_trainTypeQuestion1(self):
        assert(self._classifierType.classify(
            turbot.learn.dialog.dialogue_act_features("Do blue apples exist?"))
            == "ynQuestion")
        assert(self._classifierType.classify(
            turbot.learn.dialog.dialogue_act_features(
                "Hello")) == "Greet")
        assert(self._classifierType.classify(
            turbot.learn.dialog.dialogue_act_features(
                "You shall die!")) == "Emphasis")
        assert(self._classifierType.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What do you mean by SOS?")) == "whQuestion")
        assert(self._classifierType.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What is the color of your shoes?")) == "whQuestion")

    def test_trainTypeQuestion2(self):
        assert(self._classifierType.classify(
            turbot.learn.dialog.dialogue_act_features(
                "Do you want suggar in your coffee?")) == "ynQuestion")
        assert(self._classifierType.classify(
            turbot.learn.dialog.dialogue_act_features(
                "In which country was Obama born?")) == "whQuestion")
        assert(self._classifierType.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How long is the train ride?")) == "whQuestion")

    def test_trainWhQuestion1(self):
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features("When was the ww2?"))
            == "TimeWhen")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "When was the the world trade center bombed?")) == "TimeWhen")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "In what day was Justin Bieber born?")) == "TimeWhat")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "Where is Wally?")) == "Place")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "Where was James Bond born?")) == "Place")

    def test_trainWhQuestion2(self):
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "Who was the first singer of the Abba band?")) == "Entity")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "Who is the king of spain?")) == "Entity")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "Why did my girlfriend leave me?")) == "Reason")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "Why am I sad?")) == "Reason")

    def test_trainWhQuestion3(self):
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How do you go to the Zoo?")) == "Manner")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How should I go from the Arctic to Greenland?")) == "Manner")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What are helicopters made of?")) == "DescriptionWh")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What is the paint of my bag made of?")) == "DescriptionWh")

    def test_trainWhQuestion4(self):
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What does selfish mean?")) == "DescriptionWh")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What is the meaning of toothbrush?")) == "DescriptionWh")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What does I.S.N. stand for?")) == "DescriptionWh")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How old is Bjorn?")) == "DescriptionH")

    def test_trainWhQuestion5(self):
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How much hair does an ordinary bear have?"))
               == "DescriptionH")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What does a jew look like?")) == "DescriptionOther")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What is a dragon like?")) == "DescriptionOther")
        assert(self._classifierWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What is the form of a chain?")) == "DescriptionOther")

    def test_trainDescriptionWhQuestion(self):
        assert(self._classifierDescriptionWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What are windows made of?"))
               == "Composition")
        assert(self._classifierDescriptionWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What does meaningful mean?")) == "Meaning")
        assert(self._classifierDescriptionWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What is a banana?")) == "Meaning")
        assert(self._classifierDescriptionWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What does S.O.S. stand for?")) == "Abbreviation")
        assert(self._classifierDescriptionWh.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What is the full form of BRB?")) == "Abbreviation")

    def test_trainDescriptionHQuestion(self):
        assert(self._classifierDescriptionH.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How old are pre school kids?"))
               == "Age")
        assert(self._classifierDescriptionH.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How long does it take to travel from India to Pakistan?"))
               == "Duration")
        assert(self._classifierDescriptionH.classify(
            turbot.learn.dialog.dialogue_act_features(
                "For how long will you be in the movie?")) == "Duration")
        assert(self._classifierDescriptionH.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How many legs do mosquitos have?")) == "Quantity")
        assert(self._classifierDescriptionH.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How many guitar players does Rolling Stones have?"))
               == "Quantity")
        assert(self._classifierDescriptionH.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How frequent are the soccer matches?")) == "Frequency")
        assert(self._classifierDescriptionH.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How often do you get apples?")) == "Frequency")

    def test_trainDescriptionOtherQuestion(self):
        assert(self._classifierDescriptionOther.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How high are the Himalayas?"))
               == "Dimension")
        assert(self._classifierDescriptionOther.classify(
            turbot.learn.dialog.dialogue_act_features(
                "what is the size of your feet?"))
               == "Dimension")
        assert(self._classifierDescriptionOther.classify(
            turbot.learn.dialog.dialogue_act_features(
                "What do UFOs look like?")) == "LookAndShape")
        assert(self._classifierDescriptionOther.classify(
            turbot.learn.dialog.dialogue_act_features(
                "How does she look?")) == "LookAndShape")
