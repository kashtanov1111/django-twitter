from typing import List
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import DeleteView, TemplateView, DetailView, ListView, CreateView, RedirectView
from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.utils import timezone
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from accounts.forms import CustomUserChangeForm
from .models import Tweet
from accounts.models import Follow
from .forms import TweetCreateForm




class HomeListView(LoginRequiredMixin, ListView):
    model = Tweet

    def get_queryset(self):
        return Tweet.objects.filter(published__lte=timezone.now()).all()


class UserListView(LoginRequiredMixin, ListView):
    model = Tweet
    template_name = 'tweets/user_tweets.html'

    def get_queryset(self):
        try:
            self.tweets_user = get_user_model().objects.get(username=self.kwargs.get('username'))
        except get_user_model().DoesNotExist:
            raise Http404
        else:
            return self.tweets_user.tweets.filter(published__lte=timezone.now()).all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tweets_user'] = self.tweets_user
        self.check = self.tweets_user.followers.filter(follower_of_person=self.request.user).exists() 
        context['check'] = self.check
        return context

class Followers(LoginRequiredMixin, ListView):
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

class Following(LoginRequiredMixin, ListView):
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

@login_required
def userprofile(request):
    if request.method == 'POST':
        profile_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('tweets:user', args=[request.user.username]))
    else:
        profile_form = CustomUserChangeForm(instance=request.user)
        time = datetime.now()
    return render(request, 'account/edit_profile.html', {'profile_form': profile_form, 'time': time})


class CreateTweetView(LoginRequiredMixin, CreateView):
    model = Tweet
    form_class = TweetCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.time = timezone.now()
        context['time'] = self.time
        return context

class FollowUser(LoginRequiredMixin, RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:user', kwargs={'username': self.kwargs.get('username')})

    def get(self, request, *args, **kwargs):
        bloger = get_user_model().objects.get(username=self.kwargs.get('username'))
        try:
            Follow.objects.create(person=bloger, follower_of_person=self.request.user)
        except IntegrityError:
            Follow.objects.get(person=bloger, follower_of_person=self.request.user).delete()
        return super().get(request, *args, **kwargs)

class FollowingUser(LoginRequiredMixin, RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:following', kwargs={'username': self.kwargs.get('username1')})

    def get(self, request, *args, **kwargs):
        bloger = get_user_model().objects.get(username=self.kwargs.get('username2'))
        try:
            Follow.objects.get(person=bloger, follower_of_person=self.request.user).delete()
        except:
            Follow.objects.create(person=bloger, follower_of_person=self.request.user)
        return super().get(request, *args, **kwargs)

class FollowerUser(LoginRequiredMixin, RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:followers', kwargs={'username': self.kwargs.get('username1')})

    def get(self, request, *args, **kwargs):
        bloger = get_user_model().objects.get(username=self.kwargs.get('username2'))
        try:
            Follow.objects.get(person=bloger, follower_of_person=self.request.user).delete()
        except:
            Follow.objects.create(person=bloger, follower_of_person=self.request.user)
        return super().get(request, *args, **kwargs)

class FollowLikedByUser(LoginRequiredMixin, RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:liked_by', kwargs={'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        bloger = get_user_model().objects.get(username=self.kwargs.get('username2'))
        try:
            Follow.objects.get(person=bloger, follower_of_person=self.request.user).delete()
        except:
            Follow.objects.create(person=bloger, follower_of_person=self.request.user)
        return super().get(request, *args, **kwargs)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet

class TweetProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet

    def get_success_url(self):
        return reverse_lazy('tweets:user', kwargs={'username': self.request.user.username})

    def test_func(self):
        return self.get_object().author == self.request.user
    
class LikeHomeTweetView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:home') + '#' + str(self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        tweet = Tweet.objects.get(id=self.kwargs.get('pk'))
        if self.request.user.tweets_liked.filter(id = self.kwargs.get('pk')).exists():
            tweet.liked_by.remove(self.request.user)
        else:
            tweet.liked_by.add(self.request.user)
        return super().get(request, *args, **kwargs)

class LikeDetailTweetView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:detail', kwargs={'pk': self.kwargs.get('pk')})

    def get(self, request, *args, **kwargs):
        tweet = Tweet.objects.get(id=self.kwargs.get('pk'))
        if self.request.user.tweets_liked.filter(id = self.kwargs.get('pk')).exists():
            tweet.liked_by.remove(self.request.user)
        else:
            tweet.liked_by.add(self.request.user)
        return super().get(request, *args, **kwargs)

class LikeUserTweetsTweetView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:user', kwargs={'username': self.kwargs.get('username')}) + '#' + str(self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        tweet = Tweet.objects.get(id=self.kwargs.get('pk'))
        if self.request.user.tweets_liked.filter(id = self.kwargs.get('pk')).exists():
            tweet.liked_by.remove(self.request.user)
        else:
            tweet.liked_by.add(self.request.user)
        return super().get(request, *args, **kwargs)

class RetweetHomeView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('tweets:home') + '#' + str(self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        tweet = Tweet.objects.get(id=self.kwargs.get('pk'))
        if self.request.user.tweets_retweeted.filter(id = self.kwargs.get('pk')).exists():
            tweet.retweeted_by.remove(self.request.user)
        else:
            tweet.retweeted_by.add(self.request.user)
        return super().get(request, *args, **kwargs)

@login_required
def liked_by_tweet_view(request, pk):
    tweet = Tweet.objects.get(pk=pk)
    liked_by = tweet.liked_by.all()
    return render(request, 'tweets/liked_by.html', {'tweet': tweet, 'liked_by': liked_by})