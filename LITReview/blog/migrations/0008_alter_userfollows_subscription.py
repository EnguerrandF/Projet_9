# Generated by Django 4.1.7 on 2023-03-23 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_userfollows_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfollows',
            name='subscription',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
