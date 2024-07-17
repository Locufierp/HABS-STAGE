import pytest
import os
import shutil

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def remove_test_artifacts():
        if os.path.exists("test_output"):
            shutil.rmtree("test_output")
    request.addfinalizer(remove_test_artifacts)
