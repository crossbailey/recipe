from django.shortcuts import render
from .forms import RecipeLinkForm
from .util.scraper import get_recipe
from django.shortcuts import HttpResponse


def index(request):
    context = {'form': RecipeLinkForm()}
    return render(request, "home.html", context)


def search(request):
    if request.POST:
        recipe = (request.POST.get('recipe'))
        print(recipe)
        data_fetched = get_recipe(request.POST.get('recipe'))
        if data_fetched:
            html = "<H1> Recipe added to Recipe List! </H1>"
            return HttpResponse(html)

        if not data_fetched:
            html = "<H1> Recipe was not added to Recipe List. There was an error. Ask your husband to look into it. </H1>"
            return HttpResponse(html)
    else:
        context = {'form': RecipeLinkForm()}
        return render(request, "home.html", context)