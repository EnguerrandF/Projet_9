from django.contrib import admin
from blog.models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "image")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("headline", "user", "body")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)