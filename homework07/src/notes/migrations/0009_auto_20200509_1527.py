# Generated by Django 2.0.1 on 2020-05-09 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0008_auto_20200509_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL),
        ),
    ]
