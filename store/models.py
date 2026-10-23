from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

class Store(models.Model):
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField()
    whose = models.CharField(max_length=50)
    date_create = models.DateField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'{self.title} - {str(self.price)}, {self.whose}'