from django.db import models

# A base model that includes timestamp fields
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
class Ingredient(TimeStampedModel):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Ingredients"

    def __str__(self):
        return self.name
    
class MenuItem(TimeStampedModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='items',on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name='menu_items', blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name