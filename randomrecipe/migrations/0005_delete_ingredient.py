# Generated by Django 4.0.4 on 2022-04-30 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('randomrecipe', '0004_recipe_ingredients_recipe_instructions'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]
