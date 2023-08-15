from django.contrib import admin
from .models import User, Savings

@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'first_name', 'last_name')
@admin.register(Savings)
class Savings(admin.ModelAdmin):
    list_display = ('user', 'savings_type', 'quantity')
