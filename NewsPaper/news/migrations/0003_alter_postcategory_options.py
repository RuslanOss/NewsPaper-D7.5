# Generated by Django 4.0.4 on 2022-08-01 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_categorysubscribers_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcategory',
            options={'verbose_name': 'post category', 'verbose_name_plural': 'post categories'},
        ),
    ]
