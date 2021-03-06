from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('goals.urls', namespace='goals')),
    path('auth/', include('authentication.urls', namespace='auth')),
    path('', include('banks.urls', namespace='banks')),
    path('', include('cycles.urls', namespace='cycles'))
]
