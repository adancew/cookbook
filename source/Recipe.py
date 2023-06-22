import datetime

from fpdf import FPDF

from TagSystem import TagSystem
from Gallery import Gallery


class Recipe:

    def __init__(self, recipe_name: str):
        self.name = recipe_name
        
        self.tags = TagSystem()
        self.gallery = Gallery()
        self.is_favourite = False
        self.ingredients = []
        self.calories = 0
        self.prep_time = datetime.time(hour = 0, minute = 0, second = 0)
        self.instructions = ''

    def getTags(self):
        return self.tags.get_tags()

    def addTag(self, tag: str):
        self.tags.create_tag(tag)

    def removeTag(self, tag: str):
        self.tags.remove_tag(tag)
 
    def addPhoto(self, filename: str):
        self.gallery.addPhoto(filename)

    def removePhoto(self, filename: str):
        self.photos.remove(filename)

    def __str__(self):
        return ', '.join(["name: " + self.name, 
                  "tags: " + str(self.tags), 
                  "ingredients: " + str(self.ingredients), 
                  "calories: " + str(self.calories), 
                  "prep time: " + self.prep_time.strftime("%H:%M:%S"), 
                  "instructions: " + self.instructions,
                  "is in favourites: " + str(self.is_favourite),
                  "photos: " + str(self.gallery) + "\n"])
    
    # create a pdf based on recipe list
    def export_to_pdf(recipes, pathname):
        
        pdf = PDF_recipe('P', 'mm', 'A4') # class PDF_recipe is defined below 
        pdf.set_left_margin(30)
        pdf.set_right_margin(30)
        pdf.set_title("cookbook_" + datetime.datetime.now().strftime("%m%d%Y%H%M%S"))
        pdf.set_auto_page_break(auto = True, margin = 35)

        pdf.add_font(fname="..\\font\\DejaVuSerif.ttf")
        pdf.set_font("DejaVuSerif")
        pdf.title_page()

        # Create index page
        links = [pdf.add_link() for _ in range(len(recipes)) ]
        pdf.add_page()
        pdf.cell(0, 15, "Spis Tresci", ln = True, align='C', fill=True)

        pdf.set_font_size(12)
        for i in range(len(recipes)):
            pdf.cell(0, 10, recipes[i].name, ln = 1, link = links[i])

        # create recipe entries       
        for i in range(len(recipes)):
            pdf.print_chapter(recipes[i], link=links[i])

        pdf.output(pathname)

# end class Recipe



class PDF_recipe(FPDF):
    def header(self):
        self.ln(20)

    def footer(self):
        self.set_y(-25)
        self.set_font_size(10)
        self.cell(0, 10, f'Strona {self.page_no()}/{{nb}}', align = 'C')

    def title_page(self):
        self.add_page()
        self.set_fill_color(200, 220, 255)
        self.set_font_size(40)
        self.cell(0, 80, "Książka Kucharska", align='C', fill=True, ln=True)
        self.set_font_size(16)
        self.cell(0, 15, datetime.datetime.now().strftime("%m.%d.%Y"), 
                  align='C', fill=True, ln=True)


    def recipe_title(self, ch_title, my_link):
        self.set_link(my_link)
        self.set_font_size(20)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 15, ch_title, ln=1, fill=True, align='C', link=my_link)
        self.ln()

    def recipe_body(self, recipe: Recipe):
        self.set_text_color(0, 0, 0)
        self.set_font_size(12)
        self.ln(h=20)

        self.image(recipe.gallery.main_photo.filename, x=30, y=60, h=50) # insert photo
        self.ln(50)

        self.set_fill_color(220, 240, 255)
        self.multi_cell(0, 5, "tagi: " + str(recipe.tags))
        self.ln()
        self.multi_cell(0, 5, "kalorie: " + str(recipe.calories) + ' kcal')
        self.ln()
        self.multi_cell(0, 5, "czas przygotowania: " + 
                        recipe.prep_time.strftime("%H godz. %M min."))
        self.ln()
        self.cell(0, 5, "składniki: ", ln=1, fill=1)
        self.ln()
        self.multi_cell(0, 5, "\n".join(recipe.ingredients))
        self.ln()
        self.cell(0, 5, "instrukcje: ", ln=1, fill=1)
        self.ln()
        self.multi_cell(0, 5, recipe.instructions)
        self.ln()

        # end each chapter
        self.set_font_size(12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 5, 'KONIEC PRZEPISU')

    def print_chapter(self, recipe: Recipe, link=None):
        self.add_page()
        self.recipe_title(recipe.name, link)
        self.recipe_body(recipe)

# end class PDF_recipe
