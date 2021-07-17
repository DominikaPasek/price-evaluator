from django import forms
from django.forms import ModelForm

from .models import Category, Project, Products, SHOPS, ProjectsProducts


class CategoryForm(forms.Form):
    name = forms.CharField(label='Dodaj kategorię', max_length=64)


class NewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name']


class NewProductForm(ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'category', 'shop', 'priceFor']


# class UpdateProductsNumber(ModelForm):
#     class Meta:
#         model = ProjectsProducts
#         fields = ['number']
