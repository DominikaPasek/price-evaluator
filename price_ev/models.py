from django.db import models


SHOPS = {
    ('biltema', 'Biltema'),
    ('byggmax', 'Bygg Max'),
    ('clasohlson', 'Clas Ohlson'),
    ('flugger', 'Flügger'),
    ('jernia', 'Jernia'),
    ('jula', 'Jula'),
    ('maxbo', 'MAXBO'),
    ('monter', 'Monter'),
    ('nysted', 'NySted'),
    ('optimera', 'Optimera'),
    ('obsbygg', 'OBS Bygg'),
}


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa')
    category = models.ForeignKey(Category, verbose_name='Kategoria', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Cena', null=True)
    link = models.URLField(max_length=99, verbose_name='Link do produktu')
    shop = models.CharField(max_length=64, choices=SHOPS, default=1, verbose_name='Sklep')
    priceFor = models.CharField(max_length=15, default='szt', verbose_name='Cena za')

    def __str__(self):
        return f'{self.name} - {self.shop} - {self.price}/{self.priceFor}'


class Project(models.Model):
    name = models.CharField(max_length=64, verbose_name='Nazwa projektu')
    product = models.ManyToManyField(Products, through='ProjectsProducts')

    def __str__(self):
        return self.name


class ProjectsProducts(models.Model):
    project = models.ForeignKey(Project, verbose_name='Projekt', on_delete=models.CASCADE)
    products = models.ForeignKey(Products, verbose_name='Produkt', null=True, on_delete=models.CASCADE)
    number = models.IntegerField(default=1, verbose_name='Ilość sztuk')
    full_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Cena całkowita')
