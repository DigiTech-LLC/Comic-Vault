from django.urls import path

from . import views

urlpatterns = [
    # [url]/
    path('', views.index, name='index'),

]
