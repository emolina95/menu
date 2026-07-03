from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Category, MenuItem, Ingredient
from .serializers import CategorySerializer, IngredientSerializer, MenuItemReadSerializer, MenuItemWriteSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(is_active=True).prefetch_related('items__ingredients')
    
class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.filter(is_active=True)

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = (
        MenuItem.objects.filter(is_available=True)
        .select_related('category')
        .prefetch_related('ingredients')
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_available', 'ingredients']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return MenuItemWriteSerializer
        return MenuItemReadSerializer
    
    
