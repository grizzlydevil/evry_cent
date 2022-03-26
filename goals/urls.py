from django.urls import path, include

from rest_framework import routers

from .views import GoalsViewSet

app_name = 'goals'

router = routers.SimpleRouter()
router.register('', GoalsViewSet, basename='goal')

urlpatterns = [
    path('', include(router.urls)),
]
