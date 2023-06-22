import pytest

from source.Recipe import Recipe


class TestRecipes:

    def testInit(self):
        assert Recipe('cake').name == 'cake'
