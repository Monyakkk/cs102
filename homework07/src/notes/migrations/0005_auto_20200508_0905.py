# Generated by Django 2.0.1 on 2020-05-08 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_note_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.CharField(blank=True, max_length=511),
        ),
    ]