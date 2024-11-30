# Generated by Django 4.2.16 on 2024-11-30 19:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0004_missingperson'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_time', models.DateTimeField(auto_now_add=True)),
                ('missing_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteer.missingperson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SearchMarker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('description', models.TextField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('search_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteer.searchgroup')),
            ],
        ),
    ]
