# Generated by Django 4.0 on 2021-12-12 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_follow_followers_alter_follow_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='person',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='accounts.customuser'),
        ),
    ]