from rest_framework import routers

from .views import CycleViewSet, IncomeViewSet

app_name = 'cycles'

router = routers.DefaultRouter()
router.register('cycles', CycleViewSet, basename='cycle')
router.register('incomes', IncomeViewSet, basename='income')

urlpatterns = router.urls
