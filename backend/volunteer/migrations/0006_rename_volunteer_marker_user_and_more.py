# Generated by Django 4.2.16 on 2024-11-30 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0005_searchgroup_searchmarker'),
    ]

    operations = [
        migrations.RenameField(
            model_name='marker',
            old_name='volunteer',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='marker',
            name='description',
        ),
        migrations.AddField(
            model_name='marker',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
