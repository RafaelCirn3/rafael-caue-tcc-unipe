from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'school_name', 'city', 'state', 'xp')
    search_fields = ('username', 'email', 'school_name', 'city', 'state')
    list_filter = ('school_name', 'city', 'state')
    ordering = ('username',)

