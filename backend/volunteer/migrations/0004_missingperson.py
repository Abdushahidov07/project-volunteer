# Generated by Django 4.2.16 on 2024-11-30 09:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0003_application_applicationcharity_applyhelp_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissingPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('женщина', 'Женщина'), ('мужчина', 'Мужчина')], max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('last_known_latitude', models.FloatField()),
                ('last_known_longitude', models.FloatField()),
                ('reported_time', models.DateTimeField(auto_now_add=True)),
                ('reported_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
