from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'author_pseudonym']
    # search based on 'user__username' and 'author_pseudonym' fields
    search_fields = ['user__username', 'author_pseudonym']


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
