from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, IngredientViewSet, MenuItemViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("menu-items", MenuItemViewSet, basename="menu-item")

urlpatterns = router.urls