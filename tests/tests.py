import warnings
from pathlib import Path

import pytest


@pytest.mark.filterwarnings("ignore")
def test_dummy():
    assert 1 == 2 - 1, "Dummy test"