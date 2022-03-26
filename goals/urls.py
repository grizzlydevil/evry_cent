from django.urls import path

from .views import ListGoalsView

app_name = 'goals'
urlpatterns = [
    path('', ListGoalsView.as_view(), name='goals')
]
