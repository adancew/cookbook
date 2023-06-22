import datetime
import pickle
import os

from Recipe import Recipe
from Gallery import Photo, Gallery
from TagSystem import TagSystem

class Book:
    def __init__(self):
        self.main_gallery = Gallery 
        self.recipes = []
        self.tags = TagSystem()

    # book is an instance of a Book
    def save_book(book, filename = None):
        if isinstance(book, Book):
            if not filename: 
                timestamp = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
                filename = 'cookbook_' + timestamp
            
            with open(filename + ".pkl", "w+b") as outfile:
                pickle.dump(book, outfile)

    # returns an instance of Book or None
    def load_book(filename):
        
        try:
            with open(filename + ".pkl", "br") as infile:
                restored_book = pickle.load(infile)
        except:
            return None
        
        if isinstance(restored_book, Book):
            return restored_book
        else:
            return None

    def find_recipe(self, recipe_name):
        for recipe in self.recipes:
            if recipe.name == recipe_name:
                return recipe
        return None   

    def add_recipe(self, recipe):
        self.recipes.append(recipe)
        self.update_tags() 

    def remove_recipe(self, recipe):
        self.recipes.remove(recipe)
        self.update_tags()

    def update_tags(self):
        self.tags.clear()
        for recipe in self.recipes:
            for tag in recipe.getTags():
                self.tags.create_tag(tag)

    def get_tags(self):
        return self.tags.get_tags()
    
    def __str__(self):
        return '\n'.join([str(r) for r in self.recipes])

     