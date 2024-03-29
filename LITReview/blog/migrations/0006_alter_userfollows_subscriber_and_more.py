# Generated by Django 4.1.7 on 2023-03-22 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0005_alter_userfollows_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollows',
            name='subscriber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userfollows',
            name='subscription',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]
