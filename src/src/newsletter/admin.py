from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

from .forms import SignUpForm
from .models import SignUp, Profile


class SignUpAdmin(admin.ModelAdmin):
    list_display = ["__unicode__", "timestamp", "updated"]
    form = SignUpForm


# class Meta:
# 	model = SignUp


admin.site.register(SignUp, SignUpAdmin)


# # Define an inline admin descriptor for Employee model
# # which acts a bit like a singleton
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'profile'
#
#
# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (ProfileInline,)
#
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
