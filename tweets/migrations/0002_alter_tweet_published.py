# Generated by Django 4.0 on 2021-12-16 09:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='published',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
