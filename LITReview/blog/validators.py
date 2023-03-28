from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from blog.models import UserFollows


class ValidatorSubscription:
    message = _("Déja abonné a l'utilisateur")

    def __call__(self, value):
        if UserFollows.objects.all().filter(subscriber=settings.AUTH_USER_MODEL,
                                            subscription=value).exists():
            raise ValidationError(self.message)
