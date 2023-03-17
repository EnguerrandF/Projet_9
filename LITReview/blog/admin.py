from django.contrib import admin
from blog.models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "image")


admin.site.register(Ticket, TicketAdmin)