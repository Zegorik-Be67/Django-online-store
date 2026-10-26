from django.db import models
from django.contrib.auth.models import User

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

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    status = models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=50)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f'Заказ {self.id} - {self.user.username}, {self.total_sum}'

class OrderItem(models.Model):
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Store, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.product} x {self.quantity}'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Store, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} - {self.user.username}: {self.review}'