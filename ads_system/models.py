from django.db import models
import random

def generate_unique_id():
    # Generate an 8-digit random ID
    return random.randint(10000000, 99999999)
    
class ClassifiedAd(models.Model):
    ad_id = models.PositiveIntegerField(primary_key=True, default=generate_unique_id, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()
    ad_type = models.CharField(max_length=10, choices=[('Unitaire', 'Unitaire'), ('Pack', 'Pack')], default='single')
    bundle_items = models.TextField(blank=True)

    def __str__(self):
        return self.title
