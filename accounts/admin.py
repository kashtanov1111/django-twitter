from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Follow

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()
    list_display = ['email', 'username']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar', 'background', 'name', 'bio', 'location', 'site', 'birthday')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('avatar', 'background', 'name', 'bio', 'location', 'site', 'birthday' )}),
    )

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Follow)
