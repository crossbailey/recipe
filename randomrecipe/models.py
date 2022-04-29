from django.db import models


class Recipe(models.Model):
    name = models.TextField()
    link = models.TextField()


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.TextField(default='')
    instructions = models.TextField(default='')
