from .models import Recipes, Ingredients


r_list = [['Black Bean Burger', 'https://tasty.co/recipe/black-bean-burgers'],
          ['Carbanara', 'https://my.whisk.com/recipes/1013d120d1e2de5ed481245544a8415a8504b272660']]


recipe = Recipes(name='', link='')

Ingredients = Ingredients(recipe=recipe, ingredient='')

