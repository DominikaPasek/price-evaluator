from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from .models import Category, Project, Products, ProjectsProducts
from .forms import CategoryForm, NewProductForm, NewProjectForm
from .scrapers import *


class BasicView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "BASE.html")


class ProductsView(View):
    def get(self, request, *args, **kwargs):
        products = Products.objects.all().order_by('shop')
        cat_form = CategoryForm()
        ctx = {'cat_form': cat_form,
               'products': products}
        return render(request, 'products.html', ctx)

    def post(self, request, *args, **kwargs):
        cat_form = CategoryForm(request.POST)
        if request.POST.get('delete'):
            product_id = request.POST.get('delete')
            Products.objects.get(pk=product_id).delete()
            return redirect('/products/')
        else:
            if cat_form.is_valid():
                category = cat_form.cleaned_data['name']
                Category.objects.create(name=category)
                messages.info(request, f'Kategoria "{category}" została dodana do bazy')
                return redirect('/products/')
            else:
                products = Products.objects.all()
            return render(request, 'products.html', {'cat_form': cat_form, 'products': products})


class AddNewProduct(View):
    def get(self, request, *args, **kwargs):
        form = NewProductForm()
        return render(request, 'add_product_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = NewProductForm(request.POST)
        if form.is_valid():
            link = form.cleaned_data['link']
            shop = form.cleaned_data['shop']
            cat = form.cleaned_data['category']
            name = form.cleaned_data['name']
            price = get_price(link)
            Products.objects.create(link=link, shop=shop, category=cat, name=name, price=price)
            return redirect('products')
        else:
            return render(request, 'add_product_form.html', {'form': form})


class ProjectsList(ListView):
    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        return render(request, 'projects.html', {'projects': projects})

    def post(self, request):
        project_id = request.POST.get('delete')
        Project.objects.get(pk=project_id).delete()
        return redirect('projects')


class AddNewProject(View):
    def get(self, request, *args, **kwargs):
        form = NewProjectForm()
        return render(request, 'add_project_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = NewProjectForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            project = Project.objects.filter(name=name).first()
            return redirect(f'/projects/add-new-project/{project.id}')
        else:
            return render(request, 'add_project_form.html', {'form': form})


class AddProductsToProject(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        project = Project.objects.get(pk=pk)
        categories = Category.objects.all()
        products = Products.objects.all()
        ctx = {'project': project, 'categories': categories, 'products': products}
        return render(request, 'add_product_to_project.html', ctx)

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        project = Project.objects.get(pk=pk)
        categories = Category.objects.all()
        products = Products.objects.all()
        ctx = {'project': project, 'categories': categories, 'products': products}
        try:
            product_id = request.POST.get('prod')
            product = Products.objects.get(pk=product_id)
            number = request.POST.get('number')
            full_price = round(int(number) * product.price, 2)
            ProjectsProducts.objects.create(project=project, products=product,
                                            number=number, full_price=full_price)
            messages.info(request, 'Możesz dodać następny produkt.')
            return render(request, 'add_product_to_project.html', ctx)
        except ValueError:
            messages.info(request, 'Proszę podać wszystkie dane!')
            return render(request, 'add_product_to_project.html', ctx)


class ProjectDetails(View):
    def get(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        project = Project.objects.get(pk=project_id)
        products = ProjectsProducts.objects.filter(project=project)
        price = 0
        for product in products:
            price += product.full_price
        ctx = {'project': project, 'productss': products, 'price': price}
        return render(request, 'project.html', ctx)

    def post(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        project = Project.objects.get(pk=project_id)
        # button to delete product from project:
        if request.POST.get('delete_product'):
            product_pk = request.POST.get('delete_product')
            product = Products.objects.get(pk=product_pk)
            product_to_delete = ProjectsProducts.objects.filter(project=project, products=product)
            product_to_delete.delete()
            messages.info(request, "Produkt usunięto.")
        # button to delete the whole project:
        elif request.POST.get('delete_project'):
            project.delete()
            messages.info(request, "Projekt usunięto.")
        # input to change the number of the product in database
        elif request.POST.get('how_many_changed'):
            product_pk = request.POST.get('how_many_changed')
            product = Products.objects.get(pk=product_pk)
            how_many_products = request.POST.get('how_many')
            product_to_change = project.projectsproducts_set.get(products=product)
            # # product_to_change = ProjectsProducts.objects.filter(project=project, products=product).value()
            # product_to_change = how_many_products
            # product_to_change = how_many_products * product.price
            product_to_change.save()
        return redirect(f'/projects/{project_id}/')


def get_price(l):
    if 'biltema' in l:
        p = biltema(l)
    elif 'clasohlson' in l:
        p = clasohlson(l)
    elif 'jula' in l:
        p = jula(l)
    elif 'monter' in l:
        p = monter(l)
    elif 'nysted' in l:
        p = nysted(l)
    else:
        p = byggmax(l)
    return p
