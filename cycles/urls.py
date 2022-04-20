from rest_framework import routers

from .views import CycleViewSet, IncomeViewSet, IncomeDistributorViewSet

app_name = 'cycles'

router = routers.DefaultRouter()
router.register('cycles', CycleViewSet, basename='cycle')
router.register('incomes', IncomeViewSet, basename='income')
router.register(
    'income-distributors',
    IncomeDistributorViewSet,
    basename='income-distributor'
)

urlpatterns = router.urls
