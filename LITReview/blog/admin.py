from django.contrib import admin
from blog.models import Ticket, Review, UserFollows


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "image")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("headline", "user", "body")


class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("subscriber", "subscription", "start_date")


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsAdmin)
