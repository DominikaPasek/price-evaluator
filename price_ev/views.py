from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from .models import *
from .forms import *
from .scrapers import *
import ast


class BasicView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "BASE.html")


# Views a table of all the products:
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


# Lets you add an url needed for creation of a product:
class AddNewProductLink(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'link.html')

    def post(self, request, *args, **kwargs):
        if request.POST.get('link'):
            link = request.POST.get('link')
            request.session['link'] = link
            return redirect('/products/add-new-product/', permanent=True)
        else:
            return render(request, 'link.html')


# Second page of adding a product to the database.
class AddNewProduct(View):
    def get(self, request, *args, **kwargs):
        link = request.session.get('link')
        product_form = NewProductForm(initial={'link': link})
        if 'biltema' in link:
            data = biltema(link)
            ctx = {'data': data, 'link': link, 'form': product_form}
        else:
            price = get_price(link)
            ctx = {'price': price, 'link': link, 'form': product_form}

        request.session.clear()
        return render(request, 'add_product_form.html', ctx)

    def post(self, request, *args, **kwargs):
        link = request.POST.get('link')
        form = NewProductForm(request.POST)
        try:
            product = ast.literal_eval(request.POST.get('product'))
            price = product[1]
        except ValueError:
            price = request.POST.get('product_price')

        if form.is_valid():
            shop = form.cleaned_data['shop']
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            price_for = form.cleaned_data['priceFor']

            Products.objects.create(name=name, category=category, price=price,
                                    link=link, shop=shop, priceFor=price_for)
            messages.info(request, 'Produkt został dodany')
            return redirect('products')
        else:
            return redirect('add_new_product_link')


# Lists all projects:
class ProjectsList(ListView):
    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        return render(request, 'projects.html', {'projects': projects})

    def post(self, request):
        project_id = request.POST.get('delete')
        Project.objects.get(pk=project_id).delete()
        return redirect('projects')


# Lets you create a name for a new project:
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


# User gets to choose products needed for chosen project:
class AddProductsToProject(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        project = Project.objects.get(pk=pk)
        categories = Category.objects.all()
        products = Products.objects.all()
        added_products = ProjectsProducts.objects.filter(project=project)
        ctx = {'project': project, 'categories': categories,
               'products': products, 'added_products': added_products}
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
            full_price = int(number) * product.price
            ProjectsProducts.objects.create(project=project, products=product,
                                            number=number, full_price=full_price)
            messages.info(request, 'Możesz dodać następny produkt.')
            return render(request, 'add_product_to_project.html', ctx)
        except ValueError:
            messages.info(request, 'Proszę podać wszystkie dane!')
            return render(request, 'add_product_to_project.html', ctx)


# Summary of products prices in a project:
class ProjectDetails(View):
    def get(self, request, *args, **kwargs):
        project_id = kwargs['project_id']
        project = Project.objects.get(pk=project_id)
        products = ProjectsProducts.objects.filter(project=project)
        price = 0
        for product in products:
            price += product.full_price
        ctx = {'project': project, 'productss': products.order_by('products__name'), 'price': price}
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
            project_id = request.POST.get('delete_project')
            Project.objects.get(pk=project_id).delete()
            return redirect('projects')
            messages.info(request, "Projekt usunięto.")

        # input to change the number of the product for a project
        elif request.POST.get('which_product_to_change'):
            product_pk = request.POST.get('which_product_to_change')
            product = ProjectsProducts.objects.filter(products_id=product_pk, project=project).first()
            quantity = int(request.POST.get('quantity'))
            product.number = quantity
            product.full_price = quantity * Products.objects.get(pk=product_pk).price
            product.save()
        return redirect(f'/projects/{project_id}/')


# This function provides prices of products from given url:
def get_price(l):
    if 'clasohlson' in l:
        data = clasohlson(l)
    elif 'jula' in l:
        data = jula(l)
    elif 'monter' in l:
        data = monter(l)
    elif 'nysted' in l:
        data = nysted(l)
    else:
        data = byggmax(l)
    return data
