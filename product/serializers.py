from rest_framework import serializers
from .models import Product
from services.models import *
from .constants import FOOD_AND_PLANT_PRODUCTS, CLOTHING_PRODUCTS, ARTWORK, HANDICRAFT_PRODUCTS


from artisan.serializers import ArtisanSerializer

class ProductSerializer(serializers.ModelSerializer):
    
    artisan = ArtisanSerializer()
    
    class Meta:
        model = Product
        fields = '__all__'

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = (
            'is_verified', 'cancelled_at', 'restock_date',
            'tax_percent'
        )

    def validate_raw_material(self, value):
        if value not in dict(FOOD_AND_PLANT_PRODUCTS + CLOTHING_PRODUCTS + ARTWORK + HANDICRAFT_PRODUCTS):
            raise serializers.ValidationError("Invalid raw material type.")
        return value

    def validate_category(self, value):
        if value not in dict([
            ('food', 'Food Product'),
            ('clothing', 'Clothing Product'),
            ('artwork', 'Artwork'),
            ('handicraft', 'Handicraft Product'),
            ('other', 'Other Products')
        ]):
            raise serializers.ValidationError("Invalid category type.")
        return value

    def create(self, validated_data):
        product = super().create(validated_data)
        
        product_images = self.context.get("product_images")
        
        for imageObj in product_images:
            image = ProductImage.objects.create(product=product, image=imageObj)
            image.save()
        
        return product