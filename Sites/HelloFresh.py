import requests
import re
import json
import time


class HelloFresh():
    def __init__(self):
        self.token = HelloFresh.getToken()
        self.recipes = []

    # To get the token
    @staticmethod
    def getToken():
        url = "https://www.hellofresh.com"
        page = requests.get(url)
        page = page.text
        token = re.search("accessToken:\"(\S*)\",", page).group(1)
        return token

    # Get next 250 recipies
    def getMoreRecipes(self):
        offset = 435
        while(True):
            url = "https://gw.hellofresh.com/api/recipes/search?offset={0}&limit=1&locale=en-US&country=us".format(
                offset)
            headers = {"authorization": "Bearer " + self.token}
            data = requests.get(url, headers=headers)
            data = json.loads(data.text)
            if data['count'] == 0:
                break
            print("Fetched {0} recipes".format(data['count']))
            self.recipes += data['items']
            offset += data['count']
            time.sleep(5)
            break
        print("Finished fetching {0} recipes".format(offset))

    # Parse Tags, Ingredients, recipes
    def parseRecipes(self):
        for recipe in self.recipes:
            print("ID: {0}".format(recipe['id']))
            print("Name: {0}".format(recipe['name']))
            print("Description: {0}".format(recipe['description']))
            print("Rating: {0}".format(recipe['averageRating']))
            print("Image: {0}".format(recipe['imageLink']))
            Tags = []
            for tags in recipe['tags']:
                Tags.append(tags['name'])
            print("Tags: {0}".format(", ".join(Tags)))
            Cusine = []
            for cuisines in recipe['cuisines']:
                Cusine.append(cuisines['name'])
            print("Cusines: {0}".format(", ".join(Cusine)))
            print("Preparation Time: {0}".format(recipe['prepTime'][2:]))
            print("Nutrition:")
            for nutrition in recipe['nutrition']:
                print("\t{0}: {1} {2}".format(
                    nutrition['name'], nutrition['amount'], nutrition['unit']))
            print("Ingredients:")
            for ing in recipe['ingredients']:
                for ing_qty in recipe['yields'][0]['ingredients']:
                    if ing_qty['id'] == ing['id']:
                        print("\t{0} {1} {2}".format(
                            ing['name'], ing_qty['amount'], ing_qty['unit']))
            print("Instructions:")
            for step in recipe['steps']:
                print("Step {0}: {1}".format(step['index'], step['instructions']))
