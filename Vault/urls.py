from django.urls import path

from . import views

urlpatterns = [
    # [url]/
    path('', views.index, name='index'),

    # [url]/comic/comic_id
    path('comic/<int:id>/', views.comicpage, name='comicpage'),

    # [url]/timeline/user_profile_id
    path('timeline/<int:id>/', views.timeline, name='timeline')
    
    # [url]/profile/user_profile_id
    path('profile/<int:id>/', views.profile, name='profile')
]
