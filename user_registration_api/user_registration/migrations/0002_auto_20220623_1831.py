# Generated by Django 3.1.2 on 2022-06-23 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_address',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='active',
            new_name='is_active',
        ),
    ]
