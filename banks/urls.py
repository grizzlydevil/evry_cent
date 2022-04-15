from rest_framework import routers

from .views import BankViewSet, AccountViewSet, VaultViewSet

app_name = 'banks'

router = routers.DefaultRouter()
router.register('banks', BankViewSet, basename='bank')
router.register('accounts', AccountViewSet, basename='account')
router.register('vaults', VaultViewSet, basename='vault')

urlpatterns = router.urls
