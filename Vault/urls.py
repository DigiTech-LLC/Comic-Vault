from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # [url]/
    path('', views.index, name='index'),

    # [url]/comic/comic_id
    path('comic/<int:id>/', views.comicpage, name='comicpage'),

    # [url]/timeline/user_profile_id
    path('timeline/', views.timeline, name='timeline'),

    # [url]/profile/user_profile_id
    path('profile/<int:id>/', views.profile, name='profile'),

    # [url]/search/
    path('search/', views.search, name='search'),

    # [url]/login/
    path('login/', auth_views.login, {'template_name': 'Vault/login.html'}, name='login'),

    # [url]/logout/
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),

    # [url]/profile/user_profile_id
    path('signup/', views.signup, name='signup')

]
