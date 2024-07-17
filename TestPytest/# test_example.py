# test_example.py

import pytest

@pytest.mark.slow
def test_slow_function():
    import time
    time.sleep(5)
    assert True

def test_fast_function():
    assert True
