from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Ingredient, MenuItem


class MenuItemAPITest(APITestCase):
    def setUp(self):
        self.appetizers = Category.objects.create(name="Appetizers")
        # Ingredientes reales que aparecen en el menú
        self.bacon = Ingredient.objects.create(name="Bacon")
        self.gorgonzola = Ingredient.objects.create(name="Gorgonzola")
        self.tomato = Ingredient.objects.create(name="Tomato")
        self.hazelnuts = Ingredient.objects.create(name="Hazelnuts")
        self.parmesan = Ingredient.objects.create(name="Parmesan")

    def test_create_menu_item_with_ingredients(self):
        res = self.client.post("/api/v1/menu-items/", {
            "name": "Iceberg Wedge Salad with House Cured Bacon",
            "price": "7.50",
            "category": self.appetizers.id,
            "ingredients": [self.bacon.id, self.gorgonzola.id, self.tomato.id],
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        item = MenuItem.objects.get(name__startswith="Iceberg Wedge")
        self.assertEqual(item.ingredients.count(), 3)

    def test_read_returns_ingredient_ids(self):
        item = MenuItem.objects.create(
            name="Iceberg Wedge Salad with House Cured Bacon",
            price=Decimal("7.50"), category=self.appetizers,
        )
        item.ingredients.set([self.bacon, self.gorgonzola])

        res = self.client.get(f"/api/v1/menu-items/{item.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # tu serializer devuelve IDs, no objetos anidados
        self.assertEqual(
            set(res.data["ingredients"]),
            {self.bacon.id, self.gorgonzola.id},
        )

    def test_filter_by_ingredient(self):
        # Dos platos llevan gorgonzola, uno no → el filtro debe excluir el tercero
        iceberg = MenuItem.objects.create(
            name="Iceberg Wedge Salad with House Cured Bacon",
            price=Decimal("7.50"), category=self.appetizers,
        )
        iceberg.ingredients.set([self.bacon, self.gorgonzola, self.tomato])

        brussels = MenuItem.objects.create(
            name="Sautéed Shredded Brussels Sprouts",
            price=Decimal("6.95"), category=self.appetizers,
        )
        brussels.ingredients.set([self.bacon, self.hazelnuts, self.gorgonzola])

        kale = MenuItem.objects.create(
            name="Kale Salad",
            price=Decimal("7.50"), category=self.appetizers,
        )
        kale.ingredients.set([self.parmesan])  # sin gorgonzola

        res = self.client.get(f"/api/v1/menu-items/?ingredients={self.gorgonzola.id}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        returned = {item["name"] for item in res.data}
        self.assertEqual(
            returned,
            {
                "Iceberg Wedge Salad with House Cured Bacon",
                "Sautéed Shredded Brussels Sprouts",
            },
        )

    def test_unavailable_items_are_hidden(self):
        MenuItem.objects.create(
            name="Kale Salad", price=Decimal("7.50"),
            category=self.appetizers, is_available=True,
        )
        MenuItem.objects.create(
            name="Chicken and Cabbage Eggrolls", price=Decimal("6.95"),
            category=self.appetizers, is_available=False,
        )
        res = self.client.get("/api/v1/menu-items/")
        names = {item["name"] for item in res.data}
        self.assertEqual(names, {"Kale Salad"})

    def test_negative_price_is_rejected(self):
        # requiere el get_serializer_class corregido en el viewset
        res = self.client.post("/api/v1/menu-items/", {
            "name": "Invalid Appetizer",
            "price": "-5.00",
            "category": self.appetizers.id,
        })
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", res.data)


class CategoryAPITest(APITestCase):
    def test_category_lists_its_item_ids(self):
        appetizers = Category.objects.create(name="Appetizers")
        item = MenuItem.objects.create(
            name="Pecan Crusted Utah Goat Cheese",
            price=Decimal("6.95"), category=appetizers,
        )
        res = self.client.get(f"/api/v1/categories/{appetizers.id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # 'items' también sale como lista de IDs
        self.assertEqual(res.data["items"], [item.id])