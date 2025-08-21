from rest_framework.routers import DefaultRouter
from treasures.viewsets import BooksGenericViewSet

router = DefaultRouter()
router.register('book-xyz', BooksGenericViewSet,
basename='treasures')
print(router.urls)
urlpatterns = router.urls