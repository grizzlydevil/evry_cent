from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goals/', include('main.urls', namespace='goals')),
    path('auth/', include('auth.urls', namespace='auth'))
]
