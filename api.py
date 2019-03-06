import requests
import config
import json

def checkIfIdExists(id, site):
    r = requests.get(config.app_url + 'recipe/check/' + site + '_' + id + config.api_key).json()
    if r['exists'] == 'false':
        return False
    return True

def insert_recipe(recipe_data, image):
    files= {'photo': image }
    r = requests.post(config.app_url + 'recipe' + config.api_key, data=recipe_data, files=files).json()
    return r['id']

def insert_recipe_tags(tag_data, db_id):
    tag_data = { 'id': db_id, 'tags': tag_data}
    r = requests.post(config.app_url + 'tags' + config.api_key, json=tag_data).json()
    return r['id']

def insert_recipe_nutrition(nutrition_data, db_id):
    nutrition_data = { 'id': db_id, 'nutrition': nutrition_data}
    r = requests.post(config.app_url + 'nutrition' + config.api_key, json=nutrition_data).json()
    return r['id']

def insert_recipe_steps(step_data, db_id):
    data = {}
    files = {}
    for step in step_data:
        data['step_' + step['id']] = step['text']
        files['image_' + step['id']] = step['image']
    data['count'] = len(step_data)
    data['id'] = db_id
    r = requests.post(config.app_url + 'steps' + config.api_key, data=data, files=files).json()
    return r['id']

def insert_recipe_ingredients(ingredients_data, db_id):
    data = {}
    files = {}
    for i,ing in enumerate(ingredients_data, start=1):
        data['ing_' + str(i)] = ing['name']
        data['unit_' + str(i)] = ing['unit']
        data['value_' + str(i)] = ing['value']
        files['image_' + str(i)] = ing['image']
    data['count'] = len(ingredients_data)
    data['id'] = db_id
    r = requests.post(config.app_url + 'ingredients' + config.api_key, data=data, files=files).json()
    return r['id']