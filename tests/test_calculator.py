import pytest

from app.tools.calculator import add,divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert divide(10, 2) == 5
    assert divide(5, 0) == "Cannot divide by zero."
    