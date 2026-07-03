from rest_framework import serializers
from .models import Category, MenuItem, Ingredient


class IngredientSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'is_active']


class MenuItemReadSerializer(serializers.ModelSerializer):
    """Read: Ingredients joined"""
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'is_available', 'category', 'ingredients']

class MenuItemWriteSerializer(serializers.ModelSerializer):
    """Write: Relation by ID"""
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price', 'is_available', 'category', 'ingredients']
        
    def validate_price(self, value: float) -> float:
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'is_active', 'items']
