from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('randomrecipe.urls')),
    path('admin/', admin.site.urls),
]
