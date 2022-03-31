from django.urls import path, include

from rest_framework import routers

from .views import GoalsViewSet, WalletViewSet, PocketViewSet

app_name = 'goals'

router = routers.DefaultRouter()
router.register('goals', GoalsViewSet, basename='goals')
router.register('wallet', WalletViewSet, basename='wallet')
router.register('pocket', PocketViewSet, basename='pocket')

urlpatterns = router.urls
