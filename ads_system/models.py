from django.db import models
import random
from django.contrib.auth.models import AbstractUser

def generate_unique_id():
    # Generate an 8-digit random ID
    return random.randint(10000000, 99999999)
    
class CustomUser(AbstractUser):
    ads = models.ManyToManyField('ClassifiedAd', related_name='users', blank=True)

class Book(models.Model):
    titre = models.CharField(max_length=200, null=True)
    editeur = models.CharField(max_length=200, null=True)
    classe = models.CharField(max_length=200, null=True)
    isbn = models.IntegerField(null=True)
    matiere = models.CharField(max_length=200, null=True)
    ad = models.ForeignKey('ClassifiedAd', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.titre


class ClassifiedAd(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    ad_id = models.PositiveIntegerField(primary_key=True, default=generate_unique_id, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()
    ad_type = models.CharField(max_length=10, choices=[('Unitaire', 'Unitaire'), ('Pack', 'Pack')], default='Unitaire')
    bundle_items = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.title
    
