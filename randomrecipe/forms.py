from django import forms


class RecipeLinkForm(forms.Form):
    recipe = forms.CharField(required=False)