# Generated by Django 5.0.6 on 2024-07-05 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='con_text',
            new_name='con_message',
        ),
    ]
