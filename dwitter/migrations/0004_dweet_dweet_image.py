# Generated by Django 3.2.5 on 2023-09-04 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dwitter', '0003_profile_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='dweet',
            name='dweet_image',
            field=models.ImageField(blank=True, upload_to='photos'),
        ),
    ]
