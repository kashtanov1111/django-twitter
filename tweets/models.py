import uuid
from datetime import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.dateparse import parse_date, parse_datetime
from django.core.exceptions import ValidationError


class Tweet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='tweets')
    text = models.TextField(max_length=280)
    liked_by = models.ManyToManyField(get_user_model(), blank=True, related_name='tweets_liked')
    retweeted_by = models.ManyToManyField(get_user_model(), blank=True, related_name='tweets_retweeted')
    quote_tweeted_by = models.ManyToManyField(get_user_model(), blank=True, related_name='tweets_quote_retweeted')
    image = models.ImageField(upload_to='tweet_photos/%Y/%m/%d/', blank=True)
    published = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return self.text[:25]

    def get_absolute_url(self):
        return reverse('tweets:home')
    
    def since_published(self):
        delta_time = timezone.now() - self.published
        if delta_time.days >= 1:
            if self.published.year < timezone.now().year:
                return '%s %s' % (self.published.strftime('%d %b'), str(self.published.year))
            else:
                return '%s' % self.published.strftime('%d %b')
        else:
            if delta_time.seconds < 60:
                return '%ss' % delta_time.seconds
            if delta_time.seconds < 60 * 60:
                return '%sm' % (delta_time.seconds // 60)
            if delta_time.seconds < 60 * 60 * 24:
                return '%sh' % (delta_time.seconds // 3600)

    class Meta:
        ordering = ['-published']
