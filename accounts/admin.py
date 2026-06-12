"""Show profiles inline on the User admin page."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_orders')

    @admin.display(description='Total Orders')
    def get_orders(self, obj):
        return obj.profile.total_orders


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
