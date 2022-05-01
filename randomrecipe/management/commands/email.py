import json
import random

from django.core.management.base import BaseCommand
import unicodedata
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import csv

from randomrecipe.models import Recipe


def get_recipes():

    weekly_recipes = {"Monday": {},
                      "Tuesday": {},
                      "Wednesday": {},
                      "Thursday": {},
                      "Friday": {},
                      "Saturday": {},
                      "Sunday": {},
                      "ingredients": []
                      }

    weekly_index = {0: "Monday",
                    1: "Tuesday",
                    2: "Wednesday",
                    3: "Thursday",
                    4: "Friday",
                    5: "Saturday",
                    6 : "Sunday"}
    recipes = Recipe.objects.all()

    random_recipes = []
    count = 1
    while count <= 7:
        found = random.choice(recipes)
        if found in random_recipes:
            continue
        random_recipes.append(found)
        count += 1

    for index, recipe in enumerate(random_recipes):
        day_of_week = weekly_index[index]
        recipe_name = recipe.name
        recipe_link = recipe.link
        ingredients = recipe.ingredients
        instructions = recipe.instructions
        # Create Full list of ingredients for the weekly
        clean = []
        for ingredient in ingredients.strip('][').replace("'", "").split(', '):
            clean_string = unicodedata.normalize('NFKD', ingredient).encode('ascii', 'ignore').decode("utf-8")
            clean_string = clean_string.replace("14", "1/4").replace("12", "1/2").replace("34", "3/4").replace("13", "1/3").replace("23", "2/3")
            clean.append(clean_string)
            weekly_recipes["ingredients"].append(clean_string)

        weekly_recipes[day_of_week] = {"recipe": recipe_name,
                                       "link": recipe_link,
                                       "ingredients": clean,
                                       "instructions": instructions}

    return json.dumps(weekly_recipes, indent=4)

class Command(BaseCommand):
    def handle(self, **options):
        me = "bc2412@gmail.com"
        you = "paigetanzer@gmail.com"
        password = 'hoyxjcdsfmnxvasx'

        msg = MIMEText(get_recipes())

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = 'Weekly Recipes'
        msg['From'] = me
        msg['To'] = you

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(me, password)
        s.sendmail(me, [you], msg.as_string())
        s.quit()

        # text = """
        # Weekly Recipes.
        #
        # {table}
        #
        # """
        #
        # html = """
        # <html><body>
        # <p>Weekly Recipes</p>
        # {table}
        # </body></html>
        # """
        #
        # with open('input.csv') as input_file:
        #     reader = csv.reader(input_file)
        #     data = list(reader)
        #
        # text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
        #
        # message = MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html, 'html')])
        #
        # message['Subject'] = "Weekly Recipe"
        # message['From'] = me
        # message['To'] = me
        # server = smtplib.SMTP(server)
        # server.ehlo()
        # server.starttls()
        # server.login(me, password)
        # server.sendmail(me, you, message.as_string())
        # server.quit()
        # get_recipes()
