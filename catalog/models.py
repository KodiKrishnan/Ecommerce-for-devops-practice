from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# class Review(models.Model):
#     product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # allow null
#     rating = models.PositiveIntegerField(choices=[(i, f'{i} ★') for i in range(1, 6)])
#     comment = models.TextField(null=True, blank=True)  # allow null
#     created_at = models.DateTimeField(auto_now_add=True)



class Review(models.Model):
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, f'{i} ★') for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.rating}★ by {self.user.username}'

    