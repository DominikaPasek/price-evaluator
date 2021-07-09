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
        fields = ['link', 'shop', 'category', 'name', 'priceFor']


# class ProductToProjectForm(forms.Form):
#     project = pass
#     category = forms.ModelChoiceField(
#         queryset=Category.objects.all(),
#         label=u"Kategoria",
#         widget=ModelSelect2Widget(
#             search_fields=['name__icontains'],
#         )
#     )
#     city = forms.ModelChoiceField(
#         queryset=Products.objects.all(),
#         label=u"Produkt",
#         widget=ModelSelect2Widget(
#             search_fields=['name__icontains'],
#             dependent_fields={'category': 'category'},
#             max_results=200,
#         )
#     )
#     number = forms.NumberInput()