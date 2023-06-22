# cookbook
## Description
This project contains a program that helps keep track of user's culinary recipes. You can browse, add, delete and edit recipes. The program also allows for exporting chosen recipes to pdf, advanced filtering and searching for recipes found on the blog www.kwestiasmaku.com.
## Requirements
The program is intended to run on a desktop computer. 
It can run completely offline with the only exception exception being functionality found in "Discover" tab, which can search for new recipes on the Internet.
Program has been tested for Windows 10 and Debian 11.
## How to run the program
1. download the source code
   Can be done with command:
   $ git clone https://github.com/adancew/cookbook
   Or simply as a zip file like this:
   1.1 go to https://github.com/adancew/cookbook/
   1.2 click green button saying "Code" in upper right corner
2. extract files and run main.py like a normal python script, for example like this:
   $ python3 main.py
## Functionality   
<b>1. Home - recipe index</b>

Program opens by default in tab "Home" where you can browse recipes saved in the cookbook so far.
To the left of each recipe's name there's a checkbox. Once at least one checkbox is selected, buttons for deleting or exporting chosen recipes appear at the top of the window.

<b>2. Viewing recipe details</b>

When you click on the recipe name in recipe index, page with details opens. 
You can go back by clicking any tab (on the left)

<b>2. Editing recipe details</b>

Once in recipe details, click "edit" button at the top to edit the recipe. 

There are multiple input fields. When adding photos or tags, remember to click "Add" after entering information. If you want to remove a previously added tag or photo, click on the label with tag name or photo path.

After making changes, click "Done" button at the end of the form.

<b>3. Adding a recipe</b>

Once you click "add" tab on the left you are transported to an adding form which is same as the form for editing recipes.

<b>4. Searching and filtering</b>

At the top of the window, there is a search tab. To run the search, click the magnifying glass button next to text input field.
If you look for more advances filtering, click "filter" tab on the left.

<b>5. Looking for new recipes</b>

Click "discover" tab on the left. Enter a phrase and click search button. Wait for results. It can take a few seconds. The recipes come from culinary blog www.kwestiasmaku.com. When the search is done, you can click "open link" to go to original page or click "add recipe". If you click "add recipe", an adding form will appear with information extracted from the blig page. You can make changes to the recipe and save it in the book permanently. From now on, it will appear appear in main index even when you run the program offline.


