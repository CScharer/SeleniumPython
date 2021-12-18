import pytest


# python -m pytest -v -s
# class Example:
@pytest.mark.parametrize("field", [1, 2, 3])
def test_example(field):
    example: str = "Example"
    print(f"{example}-{field}")
    if field == 1:
        assert False, f"Testing Assertion"


def test_example2():
    example: str = "Example2"
    print(f"{example}")
    assert True, f"Testing Assertion"
