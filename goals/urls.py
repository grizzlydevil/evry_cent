from django.urls import path, include

from rest_framework import routers

from .views import GoalsViewSet, WalletViewSet

app_name = 'goals'

router = routers.DefaultRouter()
router.register('goals', GoalsViewSet, basename='goals')
router.register('wallet', WalletViewSet, basename='wallet')

urlpatterns = router.urls
