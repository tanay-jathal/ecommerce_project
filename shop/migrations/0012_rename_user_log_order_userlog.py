# Generated by Django 5.2.1 on 2025-05-15 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_rename_user_order_user_log'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='User_log',
            new_name='Userlog',
        ),
    ]
