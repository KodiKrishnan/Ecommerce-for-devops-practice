from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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

class HelpfulVote(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_helpful = models.BooleanField()

    class Meta:
        unique_together = ('review', 'user')  # one vote per user per review



# class Review(models.Model):
#     product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  # allow null
#     rating = models.PositiveIntegerField(choices=[(i, f'{i} ★') for i in range(1, 6)])
#     comment = models.TextField(null=True, blank=True)  # allow null
#     created_at = models.DateTimeField(auto_now_add=True)



class Review(models.Model):
    product = models.ForeignKey('Product', related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Temporarily nullable
    rating = models.PositiveIntegerField(choices=[(i, f'{i} ★') for i in range(1, 6)])
    comment = models.TextField(null=True, blank=True)  # Temporarily nullable
    created_at = models.DateTimeField(auto_now_add=True)

    