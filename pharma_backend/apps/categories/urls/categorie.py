from rest_framework.routers import DefaultRouter
from apps.categories.views.categorie import CategorieViewSet

router = DefaultRouter()
router.register(r'categories', CategorieViewSet, basename='categorie')

urlpatterns = router.urls
