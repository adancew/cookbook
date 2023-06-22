import sys
import os
import shutil
import datetime
from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QFileDialog
from PyQt5.QtCore import pyqtSlot

from cookbook_ui import Ui_MainWindow
from ui_utils import Ui_Index, Ui_Entry
from Recipe import Recipe

# below is necessary for Book to be successfully loaded from pickle file 
# in ui.utils.Ui_Index.create_recipes()
import Book_module
from Book_module import Book


class MainWindow(QMainWindow):

    '''
    numbering of pages stored in QStackedWidget:
    0. home - all recipes
    1. add recipe
    2. advanced filters
    3. filtering results
    4. view recipe
    5. discover - web search
    '''

    def __init__(self):
        super(MainWindow, self).__init__()

        self.book = Ui_Index.load_book('archive')
        if self.book == None: self.book = Book()

        # set up UI
        self.ui = Ui_MainWindow() # from cookbook_ui.py
        self.ui.setupUi(self)

        self.ui.icon_only_widget.hide()
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.btn_index_2.setChecked(True)
        
        self.ui.btn_delete.setHidden(True)
        self.ui.btn_export.setHidden(True)

        Ui_Index.create_filter_page(self, self.book)
        Ui_Index.create_adding_page(self, self.book)

        Ui_Index.create_recipes(self, self.book)
        Ui_Index.create_searched_recipes(self, self.book)

        self.ui.discover_status_label.setWordWrap(True)
        self.set_up_page_buttons()

    # methods for non-dynamically created buttons: ================================

    # searching
    def on_btn_search_clicked(self):
        self.ui.stackedWidget.setCurrentIndex(3)
        self.on_stackedWidget_currentChanged(3)

        search_text = self.ui.search_input.text().strip().lower()
        if search_text:
            Ui_Index.searched_recipes(self, self.book, 
                                      lambda recipe: search_text in recipe.name.lower())
        Ui_Index.reset_checkboxes(self)

    # searching on the web
    @pyqtSlot() # <- to avoid doubled execution of methods when button clicked
    def on_btn_discover_search_clicked(self):
        Ui_Index.clear_discover_results(self)
        self.ui.discover_status_label.setText("Czekaj...")
        self.ui.discover_status_label.repaint()

        search_text = self.ui.discover_input.text().strip()
        if search_text:
            Ui_Index.create_discover_page(self, search_text)
        
        if self.ui.discover_vertical_layout.count() < 3: # 3 -> input field, search btn, status label
            self.ui.discover_status_label.setText("Nie znaleziono żadnych wyników dla zapytania")
        else:
            self.ui.discover_status_label.setText("")

    # filtering
    @pyqtSlot() 
    def generate_filter_func(self):
    
        # search for phrase anywhere in recipe
        def filter_phrase(recipe):
            search_text_in = self.ui.filter_search_input.text().strip().lower()
            return (search_text_in in recipe.name.lower() or 
                    search_text_in in recipe.ingredients or 
                    search_text_in in recipe.instructions.lower())
        
        # exclude phrase anywhere in recipe
        def filter_out_phrase(recipe):
            search_text_out = self.ui.filter_exclude_input.text().strip().lower()
            if not search_text_out: return True
            
            return not (search_text_out in recipe.name.lower() or 
                    search_text_out in recipe.ingredients or 
                    search_text_out in recipe.instructions.lower())

        # search for tags
        included_tag_list = [ self.ui.included_tag_list.itemAt(index).widget().text() 
                             for index in range(0, self.ui.included_tag_list.count()) ]
        def filter_tags_included(recipe):
            for tag in included_tag_list:
                if tag not in recipe.getTags():
                    return False
            return True

        # exclude results with certain tags
        excluded_tag_list = [ self.ui.excluded_tag_list.itemAt(index).widget().text() 
                             for index in range(0, self.ui.excluded_tag_list.count()) ]
        def filter_tags_excluded(recipe):
            for tag in excluded_tag_list:
                if tag in recipe.getTags():
                    return False
            return True
        
        # check if preparation time is below maximum
        search_time = self.ui.filter_max_time_input.time().toPyTime()
        def filter_time(recipe):
            if search_time == datetime.time():
                return True
            else:
                return recipe.prep_time <= search_time

        # check if calories count is below maximum
        search_cals = self.ui.filter_max_cals_input.text()
        def filter_cals(recipe):
            if not search_cals: return True
            if search_cals.isdecimal():
                return recipe.calories <= int(search_cals)
            else:
                return False # no recipes found for incorrect input


        return lambda recipe: (filter_phrase(recipe) and 
                               filter_out_phrase(recipe) and
                               filter_tags_included(recipe) and
                               filter_tags_excluded(recipe) and
                               filter_time(recipe) and
                               filter_cals(recipe))

    @pyqtSlot()
    def on_btn_edit_clicked(self):
        recipe_name = self.ui.recipe_name.text()
        recipe = self.book.find_recipe(recipe_name)
        Ui_Entry.edit_recipe(self, recipe, self.book)
       
    # adding new recipe
    @pyqtSlot() 
    def on_btn_ready_clicked(self):
        # go back to main page
        self.ui.stackedWidget.setCurrentIndex(0)
        self.on_stackedWidget_currentChanged(0)
        self.update_header_buttons()

        # gather information from the form
        name = self.ui.form_lineEdit_name.text().strip()
        cals = self.ui.form_lineEdit_cals.text().strip()
        time = self.ui.from_timeEdit_prep.time().toPyTime()
        ingredients = self.ui.form_textEdit_ingredients.toPlainText().strip().split('\n')
        instructions = self.ui.form_textEdit_instructions.toPlainText()
        
        photos = [ self.ui.form_photo_vert.itemAt(index).widget().text() 
                             for index in range(0, self.ui.form_photo_vert.count()) ]
        
        # move photo(s) from ..\\tmp to ..\\photos so they don't get deleted
        for i in range(len(photos)):
            photo_path = photos[i]
            if photo_path:
                sections = photo_path.split("\\")
                img_filename = sections[-1]
                if len(sections) > 1: 
                    if sections[-2] == "tmp":
                        shutil.copy(photo_path, "..\\photos\\" + img_filename)
                        photos[i] = "..\\photos\\" + img_filename      


        tags = [ self.ui.form_tags_vert.itemAt(index).widget().text() 
                             for index in range(0, self.ui.form_tags_vert.count()) ]

        # clear the form for future use
        Ui_Index.clear_adding_page(self)

        # create recipe object
        recipe = Recipe(name)
        if cals.isdecimal(): recipe.calories = int(cals)
        recipe.prep_time = time
        recipe.ingredients = ingredients
        recipe.instructions = instructions
        for filename in photos: recipe.addPhoto(filename)
        for tag in tags: recipe.addTag(tag)

        # save the updated book
        self.book.add_recipe(recipe)
        self.book.save_book('archive')

        # refresh auto-completion of tags in forms
        Ui_Index.update_tag_completers(self, self.book)

        # create entries for the new recipe
        Ui_Index.create_recipe_entry(self, self.book, recipe, 
                                         self.ui.page_home, self.ui.scrollAreaWidgetContents_2, 
                                         self.ui.index_list_layout_vert)
    
        Ui_Index.create_recipe_entry(self, self.book, recipe, 
                                         self.ui.page_home, self.ui.scrollAreaContents_search, 
                                         self.ui.verticalLayout_search_results)

    # removing recipe
    @pyqtSlot() 
    def on_btn_delete_clicked(self):
        
        # if clicked on recipe details page
        if self.ui.stackedWidget.currentIndex() == 4:
            recipe_name = self.ui.recipe_name.text().strip()
            recipe = self.book.find_recipe(recipe_name)
            if recipe:
                self.book.remove_recipe(recipe)
                Ui_Index.remove_recipe_entry(self, recipe, self.ui.scrollAreaWidgetContents_2)
                Ui_Index.remove_recipe_entry(self, recipe, self.ui.scrollAreaContents_search)
               
            # go back to main page
            self.ui.stackedWidget.setCurrentIndex(0)
            self.on_stackedWidget_currentChanged(0)
        else:
            # delete entries for all selected recipes
            for page in [self.ui.scrollAreaWidgetContents_2, self.ui.scrollAreaContents_search]:
                checkboxes = [ child for child in 
                                        page.findChildren(QPushButton, "btn_index_check") ]
                names = [ child.text() for child in 
                                        page.findChildren(QPushButton, "btn_index_name") ]
                boxes_and_names = zip(checkboxes, names)
                
                for checkbox, recipe_name in list(boxes_and_names):
                    if checkbox.isChecked():
                        recipe = self.book.find_recipe(recipe_name)
                        if recipe:
                            # delete book entry for the recipe
                            self.book.remove_recipe(recipe)
                            Ui_Index.remove_recipe_entry(self, recipe, page)
                            self.update_header_buttons()
                            
        self.book.save_book('archive')
        Ui_Index.update_tag_completers(self, self.book) # refresh auto-completion of tags in forms
        Ui_Index.reset_checkboxes(self)  

    # exporting to pdf
    @pyqtSlot() 
    def on_btn_export_clicked(self):
        # open save file dialog
        home_dir = str(Path.home())
        path_name = QFileDialog.getSaveFileName(parent=self, caption='Save file', 
                                                directory=home_dir, filter="PDF Files (*.pdf)")[0]
        
        if not path_name: return None # if no filename was passed
        
        # if clicked on recipe details page
        if self.ui.stackedWidget.currentIndex() == 4:
            recipe_name = self.ui.recipe_name.text().strip()
            recipe = self.book.find_recipe(recipe_name)
            if recipe:
                Recipe.export_to_pdf([recipe], path_name)
                
        # export entries for all selected recipes   
        else:
            recipes = []
            for page in [self.ui.scrollAreaWidgetContents_2, self.ui.scrollAreaContents_search]:
                checkboxes = [ child for child in 
                                        page.findChildren(QPushButton, "btn_index_check") ]
                names = [ child.text() for child in 
                                        page.findChildren(QPushButton, "btn_index_name") ]
                boxes_and_names = zip(checkboxes, names)
                
                for checkbox, recipe_name in list(boxes_and_names):
                    if checkbox.isChecked():
                        recipe = self.book.find_recipe(recipe_name)
                        if recipe:
                            recipes.append(recipe)
            
            Recipe.export_to_pdf(recipes, path_name)

    def update_header_buttons(self):
        # loop thorugh all buttons and get their status
        checkboxes_index_page = [ (child, child.isChecked()) for child in 
                            self.ui.scrollAreaWidgetContents_2.findChildren(
                                QPushButton, "btn_index_check") ]
        checkboxes_search_page = [ (child, child.isChecked()) for child in 
                            self.ui.scrollAreaContents_search.findChildren(
                                QPushButton, "btn_index_check") ]
        
        # if any button is checked
        if (any(button[1] == True for button in checkboxes_index_page) or
                any(button[1] == True for button in checkboxes_search_page)):
            self.ui.btn_delete.setHidden(False)
            self.ui.btn_export.setHidden(False)
        else:
            self.ui.btn_delete.setHidden(True)
            self.ui.btn_export.setHidden(True)

    # changing pages
    @pyqtSlot()
    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) \
                    + self.ui.full_menu_widget.findChildren(QPushButton)
        
        # check and uncheck menu buttons
        for btn in btn_list:
            if index in [3,4,5,6]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

        Ui_Index.reset_checkboxes(self)

        # buttons for export, and delete are always visible on a recipe page
        if index == 4:
            self.ui.btn_delete.setHidden(False)
            self.ui.btn_export.setHidden(False)        

    def set_up_page_buttons(self):
        self.ui.btn_index_1.clicked.connect(self.btn_index_toggled)
        self.ui.btn_index_2.clicked.connect(self.btn_index_toggled)

        self.ui.btn_adding_1.clicked.connect(self.btn_adding_toggled)
        self.ui.btn_adding_2.clicked.connect(self.btn_adding_toggled)

        self.ui.btn_filters_1.clicked.connect(self.btn_filters_toggled)
        self.ui.btn_filters_2.clicked.connect(self.btn_filters_toggled)

        self.ui.btn_discover_1.clicked.connect(self.btn_discover_toggled)
        self.ui.btn_discover_2.clicked.connect(self.btn_discover_toggled)
   
    def btn_index_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.on_stackedWidget_currentChanged(0)

    def btn_adding_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.on_stackedWidget_currentChanged(1)

    def btn_filters_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)
        self.on_stackedWidget_currentChanged(2)

    def btn_discover_toggled(self):
        Ui_Index.clear_discover_results(self)
        self.ui.discover_input.setText("")
        self.ui.stackedWidget.setCurrentIndex(5)
        self.on_stackedWidget_currentChanged(5)

    # closing (overriden MainWindow method)
    def closeEvent(self, event):
        self.book.save_book('archive')
        for filename in os.listdir("..\\tmp"):
            os.remove("..\\tmp\\"+filename)
        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    with open("style.qss", "r") as style_file:
        style_str = style_file.read()
    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())



