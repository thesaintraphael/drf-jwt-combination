from django.contrib import admin
from django.urls import path, include
from user.views import  index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('user/', include('user.urls')),
]
