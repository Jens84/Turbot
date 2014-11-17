import turbot


def test_YesNo_basic():
    d = turbot.Dialog()
    assert(d.answer("Are you okay?") == "Yes, I am okay.")
    assert(d.answer("Are you sure?") == "No, I am not.")
    assert(d.answer("Has he a brother?") == "Yes, he has a brother.")
    assert(d.answer("Do you know him?") == "Yes, I know.")


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
