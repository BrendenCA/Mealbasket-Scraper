import requests
import re
import json
import time
import api

class HelloFresh():
    def __init__(self):
        self.token = HelloFresh.getToken()
        self.recipe_count = 0
        self.recipes = []

    # To get the token
    @staticmethod
    def getToken():
        url = "https://www.hellofresh.com"
        page = requests.get(url)
        page = page.text
        token = re.search(r"\"accessToken\":\"(\S*)\",", page).group(1)
        return token

    def getMoreRecipes(self, limit):
        url = "https://gw.hellofresh.com/api/recipes/search?offset={0}&limit={1}&locale=en-US&country=us".format(self.recipe_count, limit)
        headers = {"authorization": "Bearer " + self.token}
        data = requests.get(url, headers=headers)
        data = json.loads(data.text)
        if data['count'] == 0:
            self.recipes = []
            return False
        self.recipes = data['items']
        self.recipe_count += data['count']
        print("Finished fetching {0} recipes".format(self.recipe_count))
        return True

    def parseRecipes(self):
        while(self.getMoreRecipes(1)):
            for recipe in self.recipes:
                if api.checkIfIdExists(recipe['id'], 'hf'):
                   continue
                print("Adding ID: {0}, {1}".format(recipe['id'], recipe['name']))
                recipe_data = {}
                recipe_data['site_id'] = 'hf_' + recipe['id']
                recipe_data['name'] = recipe['name']
                recipe_data['description'] = recipe['description']
                recipe_data['rating'] = recipe['averageRating']
                recipe_data['prep_time'] = recipe['prepTime'][2:-1]
                recipe_data['difficulty'] = recipe['difficulty']
                recipe_data['approved'] = 0
                recipe_data['servings'] = recipe['yields'][0]['yields']
                image = requests.get(recipe['imageLink']).content
                db_id = api.insert_recipe(recipe_data, image)
                tag_data = []
                for tags in recipe['tags']:
                    tag_data.append(tags['name'])
                for cuisines in recipe['cuisines']:
                    tag_data.append(cuisines['name'])
                tag_data.append(recipe['category']['name'])
                api.insert_recipe_tags(tag_data, db_id)
                nutrition_data = []
                for nutrition in recipe['nutrition']:
                    nut = {}
                    nut['name'] = nutrition['name']
                    nut['value'] = nutrition['amount']
                    nut['unit'] = nutrition['unit']
                    nutrition_data.append(nut)
                api.insert_recipe_nutrition(nutrition_data, db_id)
                step_data = []
                for step in recipe['steps']:
                    s = {}
                    s['id'] = str(step['index'])
                    s['text'] = step['instructions']
                    s['image'] = requests.get(step['images'][0]['link']).content
                    step_data.append(s)
                api.insert_recipe_steps(step_data, db_id)
                ingredients_data = []
                for ing in recipe['ingredients']:
                    for ing_qty in recipe['yields'][0]['ingredients']:
                        if ing_qty['id'] == ing['id']:
                            i = {}
                            i['name'] = ing['name']
                            i['unit'] = ing_qty['unit']
                            i['value'] = ing_qty['amount']
                            i['image'] = requests.get(ing['imageLink']).content
                            ingredients_data.append(i)
                api.insert_recipe_ingredients(ingredients_data, db_id)
                print('Added')
            time.sleep(5)