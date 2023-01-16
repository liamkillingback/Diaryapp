# Generated by Django 4.1.5 on 2023-01-16 08:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diaryApp', '0005_alter_entry_options_rename_date_entry_entry_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['-date_sort']},
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='entry_date',
            new_name='date',
        ),
        migrations.AlterField(
            model_name='entry',
            name='date_sort',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]