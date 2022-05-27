# Generated by Django 3.2.6 on 2022-05-22 18:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filmes', '0002_filmes_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
