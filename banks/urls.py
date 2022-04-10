from rest_framework import routers

from .views import BankViewSet, AccountViewSet, VaultViewSet

app_name = 'banks'

router = routers.DefaultRouter()
router.register('', BankViewSet, basename='bank')
router.register('account', AccountViewSet, basename='account')
router.register('vault', VaultViewSet, basename='vault')

urlpatterns = router.urls
