from django.db import models


class Recipe(models.Model):
    name = models.TextField()
    link = models.TextField()
    ingredients = models.TextField(default='')
    instructions = models.TextField(default='')


