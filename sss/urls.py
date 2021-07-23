from django.urls import path

from sss_com.views import *

urlpatterns = [
    path('test', index, name='index'),
]