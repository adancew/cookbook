import pytest
from datetime import time

from source.Book import Book
from source.Recipe import Recipe
from source.TagSystem import TagSystem
from source.Gallery import Gallery


class TestBook:

   
    @pytest.fixture
    def recipe1(self):
        r = Recipe('cake')
        r.tags = TagSystem()
        r.photos = Gallery()
        r.ingredients = ['water', 'salt']
        r.callories = 120
        r.prep_time = time(hour = 10, minute = 34, second = 10)
        r.is_favourite = True
        return r
    
    @pytest.fixture
    def recipe2(self):
        r = Recipe('soup')
        r.tags = TagSystem()
        r.photos = Gallery()
        r.ingredients = ['veggies', 'pepper', 'mystery powder']
        r.callories = 39
        r.prep_time = time(hour = 2, minute = 24, second = 0)
        r.is_favourite = False
        return r
        

    def testInit(self, recipe1, recipe2):
        
        b = Book()
        b.recipes = [recipe1, recipe2]
        Book.save_book(b, 'testfile')
        result = Book.load_book('testfile')
        assert str(result) == str(b)

    #def testVar(self, recipe):
    #    assert recipe != None