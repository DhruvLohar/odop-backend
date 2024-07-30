from django.db import models
from .constants import *

class Product(models.Model):
    
    # PROTECT -> User cannot be deleted if they have parcels related to them
    # I can get all the parcels for the users by using related_name with user models
    
    artisan = models.ForeignKey('artisan.Artisan', related_name='listed_products', on_delete=models.PROTECT)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    back_story = models.TextField()
    price = models.PositiveIntegerField()
    is_customizable = models.BooleanField(default=False)
    custom_note = models.TextField(null=True, blank=True)
    dimensions = models.JSONField(default=dict) # length, width, height, weight 
    product_details = models.JSONField(default=dict)
    
    raw_material = models.CharField(max_length=50, choices=(
        *FOOD_AND_PLANT_PRODUCTS,
        *CLOTHING_PRODUCTS,
        *ARTWORK,
        *HANDICRAFT_PRODUCTS,
    ))
    category = models.CharField(max_length=50, choices=[
        ('food', 'Food Product'),
        ('clothing', 'Clothing Product'),
        ('artwork', 'Artwork'),
        ('handicraft', 'Handicraft Product'),
        ('other', 'Other Products')
    ])
    
    quantity = models.PositiveBigIntegerField(null=True, blank=True)
    restock_date = models.DateTimeField(null=True, blank=True)
    tax_percent = models.PositiveIntegerField(default=18)
    
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
