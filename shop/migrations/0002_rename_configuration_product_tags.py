# Generated by Django 5.1.4 on 2024-12-07 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='configuration',
            new_name='tags',
        ),
    ]
