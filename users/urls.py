from rest_framework.routers import DefaultRouter
from .views import BookViewSet, LoanViewSet, ReaderViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'readers', ReaderViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = router.urls