# Generated by Django 4.0 on 2021-12-13 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_follow_followers_follow_follower_of_person_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together={('person', 'follower_of_person')},
        ),
    ]