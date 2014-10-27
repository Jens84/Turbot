from pytest import raises
from turbot import Turbot

def test_how_are_you():
    assert Turbot("How are you?") == "Fine, and you?"
