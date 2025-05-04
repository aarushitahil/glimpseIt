from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('followers/', views.followers, name='followers'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/', views.profile, name='view-profile'),
    path('users/follow/<str:username>/', views.follow, name='follow'),
    path('users/unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('logout/', LogoutView.as_view(), name='logout'),
]