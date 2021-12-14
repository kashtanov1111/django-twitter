from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)
    background = models.ImageField(upload_to='backgrounds', blank=True, null=True)
    name = models.CharField(max_length=50, null=True)
    bio = models.CharField(max_length=160, blank=True, null=True)
    location = models.CharField(max_length=30, blank=True, null=True)
    site = models.URLField(max_length=100, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    joined = models.DateField(auto_now_add=True, null=True)

class Follow(models.Model):
    person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers', null=True)
    follower_of_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following', null=True)

    def __str__(self):
        return self.person.username

    class Meta:
        unique_together = ('person', 'follower_of_person')

