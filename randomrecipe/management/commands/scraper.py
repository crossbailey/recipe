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

        def get_recipe(link):
            ingredients_list, instructions_list, result_ingr, result_instruct, recipe_name = [], [], '', '', ''

            # create a driver for concrete page
            recipe_driver = connect(link)
            # get ingredients
            retry = 1
            while retry <= 10:
                try:
                    # Delish
                    if 'delish' in link:
                        recipe_name = link.split("/")[-2].replace("-", " ").replace("recipe", "").title()
                        result_ingr = recipe_driver.find_element(by=By.XPATH, value="/html/body/main/div[5]/div[1]/div[6]/div[1]/div[2]/div[1]/div[2]").text
                        result_instruct = recipe_driver.find_element(by=By.XPATH, value="/html/body/main/div[5]/div[1]/div[6]/div[2]/div[2]/div/div[2]/ol").text
                        recipe_driver.close()
                        break

                    # Tasty
                    elif 'tasty' in link:  # TODO tasty breaks up their ingredients per item in the recipe, can turn into dict for better viewing
                        recipe_name = link.split("/")[-1].replace("-", " ").title()
                        result_ingr = recipe_driver.find_element(by=By.XPATH, value="//*[@id='content']/div[1]/div/div[4]/div[1]/div[1]").text
                        result_instruct = recipe_driver.find_element(by=By.XPATH, value="//*[@id='content']/div[1]/div/div[4]/div[1]/div[2]/ol").text
                        recipe_driver.close()
                        break

                    # Simply Recipes
                    if 'simply' in link:
                        recipe_name = link.split("/")[-1].replace("-", " ")
                        recipe_name = ''.join([i for i in recipe_name if not i.isdigit()]).title()
                        result_ingr = recipe_driver.find_element(by=By.XPATH, value="//*[@id='structured-ingredients_1-0']/ul").text
                        result_instruct = recipe_driver.find_element(by=By.XPATH, value="//*[@id='mntl-sc-block_3-0']").text
                        recipe_driver.close()
                        break

                    # All Recipes
                    if 'all' in link:
                        recipe_name = link.split("/")[-2].replace("-", " ").title()
                        result_ingr = recipe_driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/div[5]/section[1]/fieldset/ul").text
                        result_instruct = recipe_driver.find_element(by=By.XPATH, value="/html/body/div[3]/div/main/div[1]/div[2]/div[1]/div[2]/div[2]/section[1]/fieldset/ul").text
                        recipe_driver.close()
                        break
                except Exception as e:
                    print(e)
                    retry += 1

            ingredients = result_ingr.split("\n")
            instructions = result_instruct.split("\n")

            for data in ingredients:
                if not bad_ingredients(data):
                    data = data.replace(",", "").replace(", ", "")
                    ingredients_list.append(data)

            for instruction in instructions:
                if 'simply' in link and ':' in instruction:
                    continue

                if 'all' in link and 'step ' in instruction.lower():
                    continue

                instruction = instruction.replace(",", "").replace(", ", "")
                instructions_list.append(instruction)

            print(instructions_list)
            print(ingredients_list)

            recipe = Recipe(name=recipe_name, link=link, ingredients=ingredients_list, instructions=instructions_list)
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

        get_recipe(link='https://www.allrecipes.com/recipe/8376893/chicken-chilaquiles-verdes/')
