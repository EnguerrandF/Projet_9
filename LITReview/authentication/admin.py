from django.contrib import admin
from authentication.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name")


admin.site.register(User, UserAdmin)