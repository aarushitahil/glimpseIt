""" glimpseIt URL Configuration """

from django.urls import path
from . import views

app_name = 'chat'
urlpatterns = [
    path('', views.home, name='home'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment_post'),
]