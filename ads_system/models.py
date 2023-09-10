from django.db import models

class ClassifiedAd(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField()
    ad_type = models.CharField(max_length=10, choices=[('single', 'Single Item'), ('bundle', 'Bundle')], default='single')
    bundle_items = models.TextField(blank=True)

    def __str__(self):
        return self.title
