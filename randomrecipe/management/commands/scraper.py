from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from randomrecipe.models import Recipe
from webdriver_manager.chrome import ChromeDriverManager
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        def connect(url):
            driver = webdriver.Chrome(ChromeDriverManager().install())
            try:
                driver.get(url)
            except TimeoutException:
                print('new connection try')
                driver.get(url)

            return driver

        def get_recipe(name, link):
            ingredients_list, result_ingr, result_instruct = [], '', ''

            # create a driver for concrete page
            recipe_driver = connect(link)
            # get ingredients
            retry = 1
            while retry <= 10:
                try:
                    result_ingr = recipe_driver.find_element(by=By.XPATH, value=f"//*[@id='content']/div[1]/div/div[{retry}]/div[1]/div[1]").text
                    result_instruct = recipe_driver.find_element(by=By.XPATH, value=f"//*[@id='content']/div[1]/div/div[{retry}]/div[1]/div[2]/ol").text
                    recipe_driver.close()
                    break
                except Exception:
                    retry += 1

            ingredients = result_ingr.split("\n")
            instructions_list = result_instruct.split("\n")

            for data in ingredients:
                if not bad_ingredients(data):
                    ingredients_list.append(data)

            recipe = Recipe(name=name, link=link, ingredients=ingredients_list, instructions=instructions_list)
            recipe.save()

        def bad_ingredients(data):
            ignore_ingredients = {'Nutrition', 'info', 'view', 'powered', 'ingredient', 'servings', 'salt', 'pepper',
                                  'onion', 'garlic'}

            ignore = False
            splt = set(data.split(" "))
            for bad_ingredient in ignore_ingredients:
                for char in splt:
                    if bad_ingredient.lower() in char.lower():
                        ignore = True
                        break

            return ignore

        get_recipe(name='Fajita Bowls', link='https://tasty.co/recipe/portobello-fajita-bowl-meal-prep')
