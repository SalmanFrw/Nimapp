# Generated by Django 5.0.6 on 2024-06-25 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_client_name_remove_client_updated_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='client_name',
            new_name='name',
        ),
    ]