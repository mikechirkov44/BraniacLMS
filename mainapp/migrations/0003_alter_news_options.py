# Generated by Django 4.0.4 on 2022-05-26 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_alter_news_options_rename_created_news_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'verbose_name': 'новость', 'verbose_name_plural': 'новости'},
        ),
    ]