# Generated by Django 4.2.16 on 2024-11-30 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0006_rename_volunteer_marker_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='missing_person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='volunteer.missingperson'),
        ),
    ]
