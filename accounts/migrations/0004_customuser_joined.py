# Generated by Django 4.0 on 2021-12-12 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='joined',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
