# Generated by Django 2.2.1 on 2020-05-02 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20200502_2313'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookrating',
            old_name='user',
            new_name='username',
        ),
        migrations.AlterField(
            model_name='book',
            name='rating',
            field=models.FloatField(default=None, null=True),
        ),
    ]
