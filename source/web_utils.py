from bs4 import BeautifulSoup
import requests
import re
import os

from Recipe import Recipe

class RecipeFromWeb:
    def __init__(self):
        name = ""
        link = ""
        photo_src = ""
        photo_path = ""

    
class Scrapper:
    MAX_RESULT_COUNT = 10
    ENTRIES_PER_PAGE = 20
    MAX_PAGES = MAX_RESULT_COUNT // ENTRIES_PER_PAGE

    # returns a list of bs4.element.NavigableString
    def get_search_results(search_term:str):
        
        nodes = []
        page_index = 0
        next_page = 0
        
        while next_page >= page_index and page_index <= Scrapper.MAX_PAGES:

            url = f"https://www.kwestiasmaku.com/szukaj?search_api_views_fulltext={search_term}&page={page_index}"
            try:
                page = requests.get(url).text
            except requests.exceptions.ConnectionError:
                return None
        
            doc = BeautifulSoup(page, "html.parser")
            div = doc.find(class_="view-content")

            if div: 
                nodes += div.find_all(class_="node node-przepis node-promoted node-teaser view-mode-teaser")

            # check if there are next pages
            next_btn = doc.find(class_='pagination')
            potential_next_page = re.findall('page=(.*)">', str(next_btn))
            if potential_next_page:
                next_page = int(potential_next_page[-1])
            
            page_index += 1
        
        return nodes
        
        
    # gets recipe details from divs that were returned from get_search_results 
    def get_recipe_object(node):
        links = node.find_all('a', href=True)
        
        recipe = RecipeFromWeb()
        recipe.name = links[2].contents[0]
        recipe.link = "https://www.kwestiasmaku.com" + str(links[0]['href'])
        recipe.photo_src = str(links[0].find("img")["src"])
        # download photo
        recipe.photo_path =  "..\\tmp\\" + recipe.photo_src.split('/')[-1].split('?')[0]
        if not os.path.isfile(recipe.photo_path): # check if photo already exists
            try:
                img_data = requests.get(recipe.photo_src).content
                with open(recipe.photo_path, 'wb') as handler: 
                    handler.write(img_data) 
            except requests.exceptions.ConnectionError: 
                return None
            
        return recipe
    

    def extract_tag_from_href(link):
        # links can take following forms:
        # 1. ending with html, like '/dania_dla_dwojga/party/przepisy.html' 
        # 2. or not, eg. '/przepisy/sylwester'
        # 3. or just "/przepisy.hmtl"
        # but they always start with '/'

        segments = link['href'].split('/')[1:]
        if segments[-1][-5:] != ".html":
            return segments[-1]
        else:
            if len(segments) > 1: 
                return segments[-2]
            else: 
                return segments[-1][:-5]

    # RecipeFromWeb -> Recipe
    def web_to_normal_recipe(web_recipe: RecipeFromWeb):

        recipe = Recipe(web_recipe.name)

        recipe.addPhoto(web_recipe.photo_path)

        # try to get ingredients, tags and instructions
        url = web_recipe.link
        try:
            page = requests.get(url).text
        except requests.exceptions.ConnectionError:
            return recipe
        
        doc = BeautifulSoup(page, "html.parser")
        
        # get tags
        div_tags = doc.find("div", {"id": "node-przepis-full-group-kategorie"})
        if div_tags:
            tags = [Scrapper.extract_tag_from_href(link) for link in div_tags.find_all('a', href=True)]
            for tag in tags: 
                recipe.tags.create_tag(tag)
        
        # get ingredients
        div_ingredients = doc.find(class_="field field-name-field-skladniki field-type-text-long field-label-hidden")        
        if div_ingredients: div_ingredients = div_ingredients.find("ul")
        if div_ingredients:
            ingredients = list(filter(lambda entry: entry and "li>" not in str(entry) , 
                                map(lambda entry: str(entry).strip(), 
                                    list(div_ingredients.descendants))))
            
            for ingredient in ingredients:
                recipe.ingredients.append(ingredient)
            
        # get instructions
        div_instructions = doc.find(class_="field field-name-field-przygotowanie field-type-text-long field-label-above")
        
        if div_instructions: 
            # check if instructions are in form of a list
            div_result = div_instructions.find("ul")
            if div_result:
                
                sections = list(filter(lambda entry: entry and "li>" not in entry and "strong>" not in entry, 
                                    map(lambda entry: str(entry).strip(), 
                                        list(div_result.descendants))))
                recipe.instructions = ' '.join(sections)
            else: # check if instructions are in form of paragraphs
                div_result = div_instructions.find("p")
                sections = list(filter(lambda entry: entry and "p>" not in entry, 
                                    list(div_result.descendants)))
                recipe.instructions = "\n".join(sections)
            
        return recipe
    
        

def main():
    # some example of use
    results = Scrapper.get_search_results('mimoza')
    if results:
        web_recipe = Scrapper.get_recipe_object(results[0])
        if web_recipe:
            recipe = Scrapper.web_to_normal_recipe(web_recipe)
            print(str(recipe))


if __name__ == '__main__':
    main()        