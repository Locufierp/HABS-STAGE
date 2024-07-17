# test_slow.py
import pytest

@pytest.mark.slow
def test_slow_function():
    import time
    time.sleep(1)
    assert True

@pytest.mark.fast
def test_fast_function():
    assert True