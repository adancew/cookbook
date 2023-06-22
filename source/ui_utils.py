
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTime

import os
from pathlib import Path
import webbrowser

from cookbook_ui import Ui_MainWindow
import Book_module
from Book_module import Book
from Recipe import Recipe
from web_utils import Scrapper

class Ui_Index:

    def load_book(filename: str = "testfile"):
        return Book.load_book(filename)

    def remove_recipe_entry(mainWindow, recipe: Recipe, scrollAreaWidgetContents_local):
        # get all index entries
        recipes = [ child for child in scrollAreaWidgetContents_local.
                        findChildren(QtWidgets.QWidget, "index_entry_widget")] # get all entry widgets from that layout
        
        # find entry for this particular recipe
        recipe_names = [button.text() for button in scrollAreaWidgetContents_local.
                            findChildren(QtWidgets.QPushButton, "btn_index_name") ]
        
        index = recipe_names.index(recipe.name)
        
        # remove recipe entry
        recipes[index].setParent(None)


    def create_recipe_entry(mainWindow, book: Book, recipe,
                            page, scrollAreaWidgetContents_local,
                            layout_for_entries):
        _translate = QtCore.QCoreApplication.translate

        index_entry_widget = QtWidgets.QWidget(page)
        
        index_entry_widget.setObjectName("index_entry_widget")

        index_entry_layout = QtWidgets.QHBoxLayout(index_entry_widget)
        index_entry_layout.setObjectName("index_entry_layout")

        intex_entry_inner_layout = QtWidgets.QVBoxLayout()
        intex_entry_inner_layout.setObjectName("intex_entry_inner_layout")

        # header
        intex_entry_inner_layout_header = QtWidgets.QHBoxLayout()
        intex_entry_inner_layout_header.setObjectName("intex_entry_inner_layout_header")

        # checkbox in header
        btn_index_check = QtWidgets.QPushButton(scrollAreaWidgetContents_local)
        btn_index_check.setObjectName("btn_index_check")
        btn_index_check.setMinimumSize(QtCore.QSize(0, 0))
        btn_index_check.setMaximumSize(QtCore.QSize(30, 30))
        btn_index_check.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/img/checkbox_off.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icon/img/checkbox_on.ico"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        btn_index_check.setIcon(icon)
        btn_index_check.setIconSize(QtCore.QSize(20, 20))
        btn_index_check.setCheckable(True)
        btn_index_check.setObjectName("btn_index_check")
        intex_entry_inner_layout_header.addWidget(btn_index_check)
        
        btn_index_check.toggled.connect(mainWindow.update_header_buttons)

        spacerItem = QtWidgets.QSpacerItem(100, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        intex_entry_inner_layout_header.addItem(spacerItem)
        
        # entry name in header
        btn_index_name = QtWidgets.QPushButton(scrollAreaWidgetContents_local)
        btn_index_name.setObjectName("btn_index_name")
        btn_index_name.setMinimumSize(QtCore.QSize(0, 0))
        btn_index_name.setText(_translate("MainWindow", recipe.name))

        btn_index_name.clicked.connect(lambda ch, text = btn_index_name.text() : 
                                        Ui_Entry.display_recipe(mainWindow, text, book))
        
        intex_entry_inner_layout_header.addWidget(btn_index_name)

        # time, calories
        intex_entry_inner_layout_stats = QtWidgets.QHBoxLayout()
        intex_entry_inner_layout_stats.setObjectName("intex_entry_inner_layout_stats")

        label_index_cals = QtWidgets.QLabel(scrollAreaWidgetContents_local)
        label_index_cals.setObjectName("label_index_4")

        intex_entry_inner_layout_stats.addWidget(label_index_cals)

        label_index_time = QtWidgets.QLabel(scrollAreaWidgetContents_local)
        label_index_time.setObjectName("label_index_1")

        intex_entry_inner_layout_stats.addWidget(label_index_time)

        # tags
        intex_entry_inner_layout_tags = QtWidgets.QGridLayout()
        intex_entry_inner_layout_tags.setObjectName("intex_entry_inner_layout_tags")

        # add tags in a loop
        for tag in recipe.tags.get_tags():
            label_tag = QtWidgets.QLabel(scrollAreaWidgetContents_local)
            label_tag.setObjectName("label_tag")
            intex_entry_inner_layout_tags.addWidget(label_tag)
            label_tag.setText(_translate("MainWindow", tag))

        # add to index_entry_inner_layout
        intex_entry_inner_layout.addLayout(intex_entry_inner_layout_header)
        intex_entry_inner_layout.addLayout(intex_entry_inner_layout_stats)
        intex_entry_inner_layout.addLayout(intex_entry_inner_layout_tags)
        
        spacerItem_inner_index = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        intex_entry_inner_layout.addItem(spacerItem_inner_index)
        
        index_entry_layout.addLayout(intex_entry_inner_layout)

        # photo
        label_index_photo = QtWidgets.QLabel(scrollAreaWidgetContents_local)
        label_index_photo.setMinimumSize(QtCore.QSize(200, 100))
        label_index_photo.setMaximumSize(QtCore.QSize(200, 100))
        label_index_photo.adjustSize()
        label_index_photo.setObjectName("label_index_photo")

        index_entry_layout.addWidget(label_index_photo)
        
        # finishing touch
        layout_for_entries.addWidget(index_entry_widget)

        # set contents of main layout elements

        label_index_cals.setText(_translate("MainWindow", str(recipe.calories)+" kcal"))
        label_index_time.setText(_translate("MainWindow", recipe.prep_time.strftime("%Hh %Mmin")))
        
        if recipe.gallery.main_photo is not None:
            path = recipe.gallery.main_photo.filename
            label_index_photo.setText(_translate("MainWindow", path))
            pixmap = QPixmap(path)
            label_index_photo.setPixmap(pixmap)
            label_index_photo.setScaledContents(True)
        else:
            label_index_photo.setText(_translate("MainWindow", "brak zdjęcia"))


    def create_recipes(mainWindow, book: Book):
        mw = mainWindow.ui
        for recipe in book.recipes:
            Ui_Index.create_recipe_entry(mainWindow, book, recipe, 
                                         mw.page_home, mw.scrollAreaWidgetContents_2, 
                                         mw.index_list_layout_vert)
 

    def create_searched_recipes(mainWindow, book: Book):
        mw = mainWindow.ui      
        for recipe in book.recipes:
           Ui_Index.create_recipe_entry(mainWindow, book, recipe, 
                                         mw.page_home, mw.scrollAreaContents_search, 
                                         mw.verticalLayout_search_results)
          

    def create_add_list(mainWindow, parent_layout, list_layout, line_edit_input):
        # button for adding entries to list
        def create_item():
            added_tag_text = line_edit_input.text().strip()
            line_edit_input.setText("")

            if added_tag_text != "":
                button = QtWidgets.QPushButton(parent_layout)
                button.setText(added_tag_text)
                icon = QtGui.QIcon()
                icon.addPixmap(QtGui.QPixmap(":/icon/img/close-window-64.ico"), 
                               QtGui.QIcon.Normal, QtGui.QIcon.Off)
                button.setIcon(icon)
                button.setIconSize(QtCore.QSize(16, 16))
        
                button.clicked.connect(lambda ch: button.setParent(None))
                
                list_layout.addWidget(button)

        return create_item


    # update suggestions for tags in auto-completion
    def update_tag_completers(mainWindow, book:Book):
        mw = mainWindow.ui
        tags = book.get_tags()
        mw.include_tag_input.completer().model().setStringList(tags)
        mw.exclude_tag_input.completer().model().setStringList(tags)
        mw.form_include_tag_input.completer().model().setStringList(tags)


    def reset_checkboxes(mainWindow):
        # on page change, reset checkbox buttons next to recipe names to unchecked
        for checkbox in mainWindow.ui.scrollAreaWidgetContents_2.findChildren(
                            QtWidgets.QPushButton, "btn_index_check"):
            checkbox.setChecked(False)
        for checkbox in mainWindow.ui.scrollAreaContents_search.findChildren(
                            QtWidgets.QPushButton, "btn_index_check"):
            checkbox.setChecked(False)
        mainWindow.update_header_buttons()


    def clear_filter_page(mainWindow):
        mainWindow.ui.include_tag_input.setText("")
        mainWindow.ui.exclude_tag_input.setText("")
        mainWindow.ui.filter_search_input.setText("")
        mainWindow.ui.filter_exclude_input.setText("")
        mainWindow.ui.filter_max_time_input.setTime(QTime(0,0))
        mainWindow.ui.filter_max_cals_input.setText("")

        while (mainWindow.ui.included_tag_list.count() > 0):
            mainWindow.ui.included_tag_list.itemAt(0).widget().click()
            
        while (mainWindow.ui.excluded_tag_list.count() > 0):
            mainWindow.ui.excluded_tag_list.itemAt(0).widget().click()



    def btn_run_filters_clicked(mainWindow, book: Book):
            mainWindow.ui.stackedWidget.setCurrentIndex(3)
            mainWindow.on_stackedWidget_currentChanged(3)
            Ui_Index.searched_recipes(mainWindow, mainWindow.book, 
                                      mainWindow.generate_filter_func())
            Ui_Index.clear_filter_page(mainWindow)
   

    def create_filter_page(mainWindow, book: Book):

        mw = mainWindow.ui
        
        mw.btn_run_filter_1.clicked.connect(lambda ch, mainWin = mainWindow, b = book: 
                                            Ui_Index.btn_run_filters_clicked(mainWin, b))
        mw.btn_run_filter_2.clicked.connect(lambda ch, mainWin = mainWindow, b = book: 
                                            Ui_Index.btn_run_filters_clicked(mainWin, b))
        
        
        # create auto-completion in line-edit fields
        completer = QtWidgets.QCompleter(book.get_tags())
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        mw.include_tag_input.setCompleter(completer)
        mw.exclude_tag_input.setCompleter(completer)
        
        # buttons for adding tags to lists of tags to be included or excluded
        mw.btn_include_tag.clicked.connect(lambda _ : Ui_Index.create_add_list(
            mainWindow, mw.scroll_filters_Contents, mw.included_tag_list, mw.include_tag_input)())

        mw.btn_exclude_tag.clicked.connect(lambda _ : Ui_Index.create_add_list(
            mainWindow, mw.scroll_filters_Contents, mw.excluded_tag_list, mw.exclude_tag_input)())


    def clear_adding_page(mainWindow):
        mainWindow.ui.form_lineEdit_name.setText("")
        mainWindow.ui.form_lineEdit_cals.setText("")
        mainWindow.ui.form_textEdit_ingredients.setPlainText("")
        mainWindow.ui.form_textEdit_ingredients.setPlainText("")
        mainWindow.ui.from_timeEdit_prep.setTime(QTime(0,0))
        mainWindow.ui.form_include_photo_input.setText("")
        mainWindow.ui.form_include_tag_input.setText("") 

        while (mainWindow.ui.form_tags_vert.count() > 0):
            mainWindow.ui.form_tags_vert.itemAt(0).widget().click()
            
        while (mainWindow.ui.form_photo_vert.count() > 0):
            mainWindow.ui.form_photo_vert.itemAt(0).widget().click()


    def create_adding_page(mainWindow, book: Book):
        mw = mainWindow.ui

        # create auto-completion in line-edit field for adding tags
        completer = QtWidgets.QCompleter(book.get_tags())
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        mw.form_include_tag_input.setCompleter(completer)
        
        mw.btn_form_add_tag.clicked.connect(lambda _ : Ui_Index.create_add_list(
            mainWindow, mw.scroll_adding_Contents, mw.form_tags_vert, mw.form_include_tag_input)())
        
        def set_info_from_file_dialog():
            home_dir = str(Path.home())
            path = QFileDialog.getOpenFileName(mainWindow, 'Open file', home_dir)[0]
            mw.form_include_photo_input.setText(path)

        mw.btn_photo_dialog.clicked.connect(set_info_from_file_dialog)

        mw.btn_form_add_photo.clicked.connect(lambda _ : Ui_Index.create_add_list(
            mainWindow, mw.scroll_adding_Contents, mw.form_photo_vert, mw.form_include_photo_input)())


    def create_web_recipe_entry(mainWindow, web_recipe):
        mw = mainWindow.ui
        _translate = QtCore.QCoreApplication.translate

        index_entry_widget = QtWidgets.QWidget(mw.page_discover)
        index_entry_widget.setObjectName("index_entry_widget")
        mw.discover_vertical_layout.addWidget(index_entry_widget)

        index_entry_layout = QtWidgets.QHBoxLayout(index_entry_widget)
        index_entry_layout.setObjectName("index_entry_layout")

        # left side of entry - recipe desciption
        index_entry_inner_layout = QtWidgets.QVBoxLayout()
        index_entry_inner_layout.setObjectName("intex_entry_inner_layout")
        index_entry_layout.addLayout(index_entry_inner_layout)

        # header
        label_discover_name = QtWidgets.QLabel(mw.scrollAreaContents_discover)
        label_discover_name.setObjectName("label_discover_name")
        label_discover_name.setMinimumSize(QtCore.QSize(0, 0))
        label_discover_name.setText(_translate("MainWindow", web_recipe.name))
        label_discover_name.setWordWrap(True)
        index_entry_inner_layout.addWidget(label_discover_name)

        # buttons
        intex_entry_button_layout = QtWidgets.QHBoxLayout()
        intex_entry_button_layout.setObjectName("intex_entry_button_layout")
        index_entry_inner_layout.addLayout(intex_entry_button_layout)

        btn_open_link = QtWidgets.QPushButton(mw.scrollAreaContents_discover)
        btn_open_link.setObjectName("btn_open_link")
        btn_open_link.setMinimumSize(QtCore.QSize(100, 0))
        btn_open_link.setMaximumSize(QtCore.QSize(150, 30))
        btn_open_link.setText("otwórz link")
        btn_open_link.clicked.connect(lambda ch, url = web_recipe.link : webbrowser.open(url))

        btn_add_to_book = QtWidgets.QPushButton(mw.scrollAreaContents_discover)
        btn_add_to_book.setObjectName("btn_add_to_book")
        btn_add_to_book.setMinimumSize(QtCore.QSize(100, 0))
        btn_add_to_book.setMaximumSize(QtCore.QSize(150, 30))
        btn_add_to_book.setText("dodaj do książki")

        btn_add_to_book.clicked.connect(lambda ch, recipe = Scrapper.web_to_normal_recipe(web_recipe) : 
                                      Ui_Entry.add_recipe_from_web(mainWindow, recipe))

        
        # spacer to align buttons to the left
        button_spacer = QtWidgets.QSpacerItem(50, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        intex_entry_button_layout.addWidget(btn_open_link)
        intex_entry_button_layout.addWidget(btn_add_to_book)
        intex_entry_button_layout.addItem(button_spacer)

        inner_layout_spacer = QtWidgets.QSpacerItem(10, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        index_entry_inner_layout.addItem(inner_layout_spacer)
            
        # right side of entry - photo
        label_index_photo = QtWidgets.QLabel(mw.scrollAreaContents_discover)
        label_index_photo.setMinimumSize(QtCore.QSize(200, 200))
        label_index_photo.setMaximumSize(QtCore.QSize(200, 200))
        label_index_photo.setObjectName("label_index_photo")

        pixmap = QPixmap(web_recipe.photo_path)
        label_index_photo.setPixmap(pixmap)
        
        index_entry_layout.addWidget(label_index_photo)

   
    def clear_discover_results(mainWindow):
        mw = mainWindow.ui
        
        for filename in os.listdir("..\\tmp"):
            os.remove("..\\tmp\\"+filename)

        mw.discover_status_label.setText("")
        # itemAt(0) - layout for search
        # itemAt(1) - label with status (eg. 'searching...', 'nothing found')
        # remaining items are results of previous search
        entries = [mw.discover_vertical_layout.itemAt(index) for index 
                   in range(0, mw.discover_vertical_layout.count())]
        for entry in entries[2:]: entry.widget().setParent(None)


    def create_discover_page(mainWindow, search_text: str):
        raw_results = Scrapper.get_search_results(search_text)
        if raw_results:
            for raw_result in raw_results:
                web_recipe = Scrapper.get_recipe_object(raw_result)
                if web_recipe:
                    Ui_Index.create_web_recipe_entry(mainWindow, web_recipe)
       
    
    # hide recipes that are filtered out
    def searched_recipes(mainWindow, book: Book, filter_func):
        mw = mainWindow.ui
        index = mw.verticalLayout_search_results.count()

        while(index > 0):
            myWidget = mw.verticalLayout_search_results.itemAt(index - 1).widget()
            
            if not filter_func(book.recipes[index - 1]): 
                myWidget.hide()
            else:
                myWidget.show()
            index -=1
            


class Ui_Entry:

    def edit_recipe(mainWindow, recipe, book):
        # overwrite fields in page with adding recipe form with current recipe values
        mainWindow.ui.form_lineEdit_name.setText(recipe.name)
        mainWindow.ui.form_lineEdit_cals.setText(str(recipe.calories))
        mainWindow.ui.form_textEdit_ingredients.setPlainText('\n'.join(recipe.ingredients))
        mainWindow.ui.form_textEdit_ingredients.setPlainText(recipe.instructions)

        hours = recipe.prep_time.hour
        minutes = recipe.prep_time.minute
        mainWindow.ui.from_timeEdit_prep.setTime(QtCore.QTime(hours, minutes))

        for photo in recipe.gallery.photos:
            mainWindow.ui.form_include_photo_input.setText(photo.filename)
            mainWindow.ui.btn_form_add_photo.click()

        for tag in recipe.getTags():
            mainWindow.ui.form_include_tag_input.setText(tag)
            mainWindow.ui.btn_form_add_tag.click()       
                
        # remove current recipe from the book
        book.remove_recipe(recipe)
        Ui_Index.remove_recipe_entry(mainWindow, recipe, mainWindow.ui.scrollAreaWidgetContents_2)
        Ui_Index.remove_recipe_entry(mainWindow, recipe, mainWindow.ui.scrollAreaContents_search)
        Ui_Index.reset_checkboxes(mainWindow)
        # go to page with form for adding new recipe
        mainWindow.ui.stackedWidget.setCurrentIndex(1)
        mainWindow.on_stackedWidget_currentChanged(1)


    def add_recipe_from_web(mainWindow, recipe: Recipe):
        # overwrite fields in page with adding recipe form with current recipe values
        mainWindow.ui.form_lineEdit_name.setText(recipe.name)
        mainWindow.ui.form_textEdit_ingredients.setPlainText('\n'.join(recipe.ingredients))
        mainWindow.ui.form_textEdit_instructions.setPlainText(recipe.instructions)

        for photo in recipe.gallery.photos:
            mainWindow.ui.form_include_photo_input.setText(photo.filename)
            mainWindow.ui.btn_form_add_photo.click()

        for tag in recipe.getTags():
            mainWindow.ui.form_include_tag_input.setText(tag)
            mainWindow.ui.btn_form_add_tag.click()       
        
        # go to page with form for adding new recipe
        mainWindow.ui.stackedWidget.setCurrentIndex(1)
        mainWindow.on_stackedWidget_currentChanged(1)


    def display_recipe(mainWindow: Ui_MainWindow, recipe_name: str, book: Book):

        mw = mainWindow.ui
        _translate = QtCore.QCoreApplication.translate

        mainWindow.on_stackedWidget_currentChanged(4)
        mw.stackedWidget.setCurrentIndex(4)

        recipe = book.find_recipe(recipe_name)
        if recipe:
            mw.recipe_name.setText(_translate("MainWindow", recipe.name))
            mw.recipe_cals.setText(_translate("MainWindow", "kalorie: "+str(recipe.calories)))
            mw.recipe_time.setText(_translate("MainWindow", "czas przygotowania: " + 
                                                recipe.prep_time.strftime("%Hh %Mmin")))
            mw.recipe_ingredients.setText(_translate("MainWindow", 
                                                     "składniki: \n- " + "\n- ".join(recipe.ingredients)))
            mw.recipe_instructions.setText(_translate("MainWindow", 
                                                      "instrukcje: \n" + recipe.instructions))
        
        