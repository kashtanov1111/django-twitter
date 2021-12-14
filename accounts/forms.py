from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm, UserCreationForm
from allauth.account.forms import SignupForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'name')

class CustomUserChangeForm(UserChangeForm):
    avatar = forms.ImageField(widget=forms.FileInput, required=False)
    background = forms.ImageField(widget=forms.FileInput, required=False)
    site = forms.URLField(initial="http://", widget=forms.TextInput, required=False)
    password = None
    class Meta:
        model = get_user_model()
        fields = ('background', 'avatar', 'username', 'name', 'bio', 'location', 'site', 'birthday', 'email')

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=50, required=True)
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.save()
        return user
    