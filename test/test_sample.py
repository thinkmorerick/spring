import pytest


def add(a, b):
    """return a + b

    Args:
        a (int): int
        b (int): int

    Returns:
        a + b

    Raises:
        AssertionError: if a or b is not integer

    """
    assert all([isinstance(a, int), isinstance(b, int)])
    return a + b


def test_add():
    assert add(1, 2) == 3
    assert isinstance(add(1, 2) , int)
    with pytest.raises(Exception):    # test exception
        add('1', 2)