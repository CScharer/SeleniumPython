import pytest


# python -m pytest -v -s
class TestExample:
    @pytest.mark.parametrize("field", [1, 2, 3])
    def test_example(self, field):
        example: str = "Example"
        print(f"{example}-{field}")
        if field == 1:
            assert False, f"Testing Assertion"

    def test_example2(self):
        example: str = "Example2"
        print(f"{example}")
        assert True, f"Testing Assertion"
