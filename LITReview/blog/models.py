from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class Ticket(models.Model):
    title = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=10000, blank=False)
    image = models.ImageField(upload_to='image_ticket/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE)


class Review(models.Model):
    RATING_SELECT = (
        (0, 'Note 0'),
        (1, 'Note 1'),
        (2, 'Note 2'),
        (3, 'Note 3'),
        (4, 'Note 4'),
        (5, 'Note 5'),
    )

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        choices=RATING_SELECT,
        validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    subscriber = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    subscription = models.CharField(max_length=128, blank=False, null=True)
    start_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('subscriber', 'subscription')

