from src.calculator import add

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 5) == 0
    assert add(0, 0) == 0
