# Generated by Django 2.2.1 on 2020-05-02 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='bio',
        ),
    ]
