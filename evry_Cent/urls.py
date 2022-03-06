from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('goals/', include('goals.urls', namespace='goals')),
    path('auth/', include('authentication.urls', namespace='auth'))
]
