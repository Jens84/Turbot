""" Script containing pytest unit test for turbot."""

from turbot import Turbot
import unittest
import pytest


class TurbotTest(unittest.TestCase):
    _t = None
    _c = None

    @pytest.fixture(autouse=True)
    def init(self):
        self._t = Turbot()
        self._c = self._t.getClassifier()

    def test_YesNo_basic(self):
        assert(self._t.answer("Are you okay?") == "Yes, I am okay.")
        assert(self._t.answer("Are you sure?") == "No, I am not sure.")
        assert(self._t.answer("Has he a brother?") == "Yes, he has a brother.")
        assert(self._t.answer("Do you know him?") == "Yes, I know him.")
        assert(self._t.answer("Are they fine?") == "Yes, they are fine.")

    def test_YesNo_complex(self):
        assert(self._t.answer("Is Barack Obama the president?")
               == "Yes, Barack Obama is the president.")
        assert(self._t.answer("Do you know Francois Hollande?")
               == "Yes, I know Francois Hollande.")
        assert(self._t.answer("Have you been at school?")
               == "No, I have not been at school.")
        assert(self._t.answer("Has he a brother?") == "Yes, he has a brother.")

    def test_YesNo_tenses(self):
        assert(self._t.answer("Have you been at school?")
               == "No, I have not been at school.")
        assert(self._t.answer("Will you see the movie?")
               == "Yes, I will see the movie.")
        assert(self._t.answer("Did you play tennis")
               == "Yes, I played tennis.")

    def test_YesNo_wikipedia(self):
        assert(self._t.answer("Is Merkel a singer?")
               == "No, Merkel is not a singer.")
        assert(self._t.answer("Is Obama the president?")
               == "Yes, Obama is the president.")
        assert(self._t.answer("Is Paris in France?")
               == "Yes, Paris is in France.")
        assert(self._t.answer("Is London in United Kingdom?")
               == "Yes, London is in United Kingdom.")

    def test_Markov(self):
        answer1 = self._t.answer("I love you")
        assert("I" in answer1 and "love" in answer1)

    def test_trainTypeQuestion1(self):
        assert(self._t.sentenceType("Do blue apples exist?")
               == "ynQuestion")
        assert(self._t.sentenceType("Hello") == "Greet")
        assert(self._t.sentenceType("You shall die!") == "Emphasis")
        assert(self._t.sentenceType("What do you mean by SOS?")
               == "whQuestion")
        assert(self._t.sentenceType("What is the color of your shoes?")
               == "whQuestion")

    def test_trainTypeQuestion2(self):
        assert(self._t.sentenceType("Do you want suggar in your coffee?")
               == "ynQuestion")
        assert(self._t.sentenceType("In which country was Obama born?")
               == "whQuestion")
        assert(self._t.sentenceType("How long is the train ride?")
               == "whQuestion")

    def test_trainWhQuestion1(self):
        assert(self._c.classifyWhType("When was the ww2?") == "TimeWhen")
        assert(self._c.classifyWhType(
               "When was the the world trade center bombed?") == "TimeWhen")
        assert(self._c.classifyWhType(
               "In what day was Justin Bieber born?") == "TimeWhat")
        assert(self._c.classifyWhType(
               "Where is Wally?") == "Place")
        assert(self._c.classifyWhType(
               "Where was James Bond born?") == "Place")

    def test_trainWhQuestion2(self):
        assert(self._c.classifyWhType(
               "Who was the first singer of the Abba band?") == "Entity")
        assert(self._c.classifyWhType(
               "Who is the king of spain?") == "Entity")
        assert(self._c.classifyWhType(
               "Why did my girlfriend leave me?") == "Reason")
        assert(self._c.classifyWhType(
               "Why am I sad?") == "Reason")

    def test_trainWhQuestion3(self):
        assert(self._c.classifyWhType(
               "How do you go to the Zoo?") == "Manner")
        assert(self._c.classifyWhType(
               "How should I go from the Arctic to Greenland?") == "Manner")
        assert(self._c.classifyWhType(
               "What are helicopters made of?") == "DescriptionWh")
        assert(self._c.classifyWhType(
               "What is the paint of my bag made of?") == "DescriptionWh")

    def test_trainWhQuestion4(self):
        assert(self._c.classifyWhType(
               "What does selfish mean?") == "DescriptionWh")
        assert(self._c.classifyWhType(
               "What is the meaning of toothbrush?") == "DescriptionWh")
        assert(self._c.classifyWhType(
               "What does I.S.N. stand for?") == "DescriptionWh")
        assert(self._c.classifyWhType(
               "How old is Bjorn?") == "DescriptionH")

    def test_trainWhQuestion5(self):
        assert(self._c.classifyWhType(
               "How much hair does an ordinary bear have?")
               == "DescriptionH")
        assert(self._c.classifyWhType(
               "What does a jew look like?") == "DescriptionOther")
        assert(self._c.classifyWhType(
               "What is a dragon like?") == "DescriptionOther")
        assert(self._c.classifyWhType(
               "What is the form of a chain?") == "DescriptionOther")

    def test_trainDescriptionWhQuestion(self):
        assert(self._c.classifyDescWhQ("What are windows made of?")
               == "Composition")
        assert(self._c.classifyDescWhQ("What does meaningful mean?")
               == "Meaning")
        assert(self._c.classifyDescWhQ("What is a banana?")
               == "Meaning")
        assert(self._c.classifyDescWhQ("What does S.O.S. stand for?")
               == "Abbreviation")
        assert(self._c.classifyDescWhQ("What is the full form of BRB?")
               == "Abbreviation")

    def test_trainDescriptionHQuestion(self):
        assert(self._c.classifyDescHQ("How old are pre school kids?")
               == "Age")
        assert(self._c.classifyDescHQ(
               "How long does it take to travel from India to Pakistan?")
               == "Duration")
        assert(self._c.classifyDescHQ("For how long will you be in the movie?")
               == "Duration")
        assert(self._c.classifyDescHQ("How many legs do mosquitos have?")
               == "Quantity")
        assert(self._c.classifyDescHQ(
               "How many guitar players does Rolling Stones have?")
               == "Quantity")
        assert(self._c.classifyDescHQ("How frequent are the soccer matches?")
               == "Frequency")
        assert(self._c.classifyDescHQ("How often do you get apples?")
               == "Frequency")

    def test_trainDescriptionOtherQuestion(self):
        assert(self._c.classifyDescOtherQ("How high are the Himalayas?")
               == "Dimension")
        assert(self._c.classifyDescOtherQ("what is the size of your feet?")
               == "Dimension")
        assert(self._c.classifyDescOtherQ("What do UFOs look like?")
               == "LookAndShape")
        assert(self._c.classifyDescOtherQ("How does she look?")
               == "LookAndShape")

    def test_whoQuestion(self):
        assert(self._t.answer("Who is Obama?")
               == "Obama is a Illinois.")

    def test_whenQuestion(self):
        assert(self._t.answer("When did Picasso die?")
               == "Picasso died on the 1973-04-08+02:00.")
        assert(self._t.answer("When was Claude Monet born?")
               == "Claude Monet was born on the 1840-11-14+02:00.")
        assert(self._t.answer("At what time was Claude Monet born?")
               == "Claude Monet was born  1840-11-14+02:00.")

    def test_whatQuestion(self):
        assert(self._t.answer("What color is tomato?")
               == "The tomato plant itself is green. The fruit ",
               "of most tomato varieties starts out green in ",
               "color and matures to some shade of red, or ",
               "pinkish-red. Some varieties, though, ripen ",
               "to yellow and some to a deep burgundy color.")
        assert(self._t.answer("What is the capital of France?")
               == "The capital of France is  Paris.")
        assert("Unless you are looking at a nearby object like the earth ",
               "or moon it is solid black except for stars"
               in self._t.answer("What does the space look like?"))
        assert("Human act of combat against an opposing side that ",
               "results in the deaths of many and control of money, ",
               "power, and government."
               in self._t.answer("What does war mean?"))
        assert(self._t.answer("What is the full form of NASA?")
               == "It's National Aeronautics and Space Administration.")

    def test_whereQuestion(self):
        assert(self._t.answer("Where is the England?")
               == "The England is in 51.5 -0.11666666666666667.")

    def test_whyQuestion(self):
        assert("Sunlight interacting with the Earth's atmosphere ",
               "makes the sky blue." in self._t.answer("Why is the sky blue?"))

    def test_howQuestion(self):
        assert(self._t.answer("How do you go to school?")
               == "You can take the bus,ride a bike,walk,take a car,",
                  "ride a scooter,take a taxi or not go at all i prefer to ",
                  "walk because walking gives you energy but when you take ",
                  "vehicle's it just wastes your energy.")
        assert(self._t.answer("How high is the Eiffel Tower?")
               == "The Eiffel Tower is by 300.")
        assert(self._t.answer("How old is Justin Bieber?")
               == "Justin Bieber is 20 years old (birthdate: March 1, 1994).")
        assert("Cooking small roasts can be difficult if you ",
               "use standard rules of thumb like 15 min per lb"
               in self._t.answer("How long does it take to cook beef?"))
        assert(self._t.answer("How many neurons does a brain have?")
               == "About 1,000,000,000. Or one billion.\n\n100 billion neuron",
                  " cells re in the brainThere are approximately 100 billion ",
                  "neurons in the human brain.")
        assert(self._t.answer("How often do you shave?")
               == "I\'m a man and I shave every 1 to 4 days depending on ",
                  "what I feel like and if my wife thinks I look \"grubby\".")
