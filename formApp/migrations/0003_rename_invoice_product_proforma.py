# Generated by Django 5.0.1 on 2024-04-01 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formApp', '0002_delete_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='invoice',
            new_name='proforma',
        ),
    ]
