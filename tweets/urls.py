from django.http.response import HttpResponse
from django.urls import path
from django.shortcuts import HttpResponse
from . import views

app_name = 'tweets'
urlpatterns = [
    path('', views.HomeListView.as_view(), name='home'),
    path('edit-profile/', views.userprofile, name='edit'),
    path('new-tweet/', views.CreateTweetView.as_view(), name='new_tweet'),
    path('<uuid:pk>/',views.TweetDetailView.as_view(), name='detail'),
    path('<str:username>/', views.UserListView.as_view(), name='user'),
    path('<str:username>/followers/', views.Followers.as_view(), name='followers'),
    path('<str:username>/following/', views.Following.as_view(), name='following'),
    path('follow/<str:username>/', views.FollowUser.as_view(), name='follow'),
    path('following/<str:username1>/<str:username2>/', views.FollowingUser.as_view(), name='following_unfollow'),
    path('follower/<str:username1>/<str:username2>/', views.FollowerUser.as_view(), name='follower_unfollow'),
    
]
