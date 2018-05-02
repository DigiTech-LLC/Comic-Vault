from django.urls import path

from . import views

urlpatterns = [
    # [url]/
    path('', views.index, name='index'),

    # [url]/comic_id
    path('comic/<int:id>/', views.comicpage, name='comicpage'),
]
