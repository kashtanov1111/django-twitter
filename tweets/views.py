from typing import List
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, RedirectView
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError


from accounts.forms import CustomUserChangeForm
from .models import Tweet
from accounts.models import Follow





class HomeListView(ListView):
    model = Tweet



class UserListView(ListView):
    model = Tweet
    template_name = 'tweets/user_tweets.html'

    def get_queryset(self):
        try:
            self.tweets_user = get_user_model().objects.get(username=self.kwargs.get('username'))
        except get_user_model().DoesNotExist:
            raise Http404
        else:
            return self.tweets_user.tweets.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tweets_user'] = self.tweets_user
        self.check = self.tweets_user.followers.filter(follower_of_person=self.request.user).exists() 
        context['check'] = self.check
        return context

class Followers(ListView):
    model = Follow
    template_name = 'tweets/followers.html'

    def get_queryset(self):
        try:
            self.tweets_user = get_user_model().objects.get(username=self.kwargs.get('username'))
        except get_user_model().DoesNotExist:
            raise Http404
        else:
            return self.tweets_user.followers.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tweets_user'] = self.tweets_user
        return context

class Following(ListView):
    model = Follow
    template_name = 'tweets/following.html'

    def get_queryset(self):
        try:
            self.tweets_user = get_user_model().objects.get(username=self.kwargs.get('username'))
        except get_user_model().DoesNotExist:
            raise Http404
        else:
            return self.tweets_user.following.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tweets_user'] = self.tweets_user
        return context


def userprofile(request):
    if request.method == 'POST':
        profile_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('tweets:user', args=[request.user.username]))
    else:
        profile_form = CustomUserChangeForm(instance=request.user)
    return render(request, 'account/edit_profile.html', {'profile_form': profile_form})


class CreateTweetView(CreateView):
    model = Tweet
    fields = ('text', 'image', 'published')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

class FollowUser(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:user', kwargs={'username': self.kwargs.get('username')})

    def get(self, request, *args, **kwargs):
        bloger = get_user_model().objects.get(username=self.kwargs.get('username'))
        try:
            Follow.objects.create(person=bloger, follower_of_person=self.request.user)
        except IntegrityError:
            Follow.objects.get(person=bloger, follower_of_person=self.request.user).delete()
        return super().get(request, *args, **kwargs)

class FollowingUser(RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:following', kwargs={'username': self.kwargs.get('username1')})

    def get(self, request, *args, **kwargs):
        bloger = get_user_model().objects.get(username=self.kwargs.get('username2'))
        try:
            Follow.objects.get(person=bloger, follower_of_person=self.request.user).delete()
        except:
            Follow.objects.create(person=bloger, follower_of_person=self.request.user)
        return super().get(request, *args, **kwargs)