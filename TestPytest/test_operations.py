from operator import addition, soustraction

def test_addition():
    assert addition(3, 5) == 8
    assert addition(1, 0) == 1
    assert addition(5, -8) == -3


def test_soustraction():
    assert soustraction(8, 5) == 3
    assert soustraction(5, 8) == -3
    assert soustraction(1, 0) == 1
    assert soustraction(3, -5) == 8