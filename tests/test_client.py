from cardazim.Card import Card
import pytest


@pytest.mark.parametrize('name, creator, path, riddle, solution',
                         ["card", "Omri", "/home/user/Pictures/panda.jpg", "what?", "HA HA!"])
def test_serialize(name: str, creator: str, path: str, riddle: str, solution: str):
    card = Card.create_from_path(name, creator, path, riddle, solution)
    data = card.serialize()
    card2 = Card.deserialize(data)
    assert (card2.solution is None)
    assert (card2.serialize() == data)
    card2.solution = solution
    assert (repr(card) == repr(card2))
    assert (str(card) == str(card2))


@pytest.mark.parametrize('name, creator, path, riddle, solution',
                         ["card", "Omri", "/home/user/Pictures/panda.jpg", "what?", "HA HA!"])
def test_cripto(name: str, creator: str, path: str, riddle: str, solution: str):
    card = Card.create_from_path(name, creator, path, riddle, solution)
    card.image.encrypt(card.solution)
    card.image.image.show()
    data = card.serialize()
    card2 = Card.deserialize(data)
    if card2.image.decrypt(solution):
        card2.solution = solution
    assert (repr(card) == repr(card2))
    assert (card.image.decrypt(solution))
    assert (card.serialize() == card2.serialize())
