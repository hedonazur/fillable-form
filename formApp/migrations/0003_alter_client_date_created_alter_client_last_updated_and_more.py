# Generated by Django 5.0.1 on 2024-03-11 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formApp', '0002_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='date_created',
            field=models.DateTimeField(blank=True, help_text='Not to fill', null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_updated',
            field=models.DateTimeField(blank=True, help_text='Not to fill', null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='slug',
            field=models.SlugField(blank=True, help_text='Not to fill', max_length=500, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='uniqueId',
            field=models.CharField(blank=True, help_text='Not to fill', max_length=100, null=True),
        ),
    ]
