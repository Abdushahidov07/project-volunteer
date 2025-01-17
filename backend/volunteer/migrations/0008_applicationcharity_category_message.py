# Generated by Django 4.2.16 on 2024-12-01 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('volunteer', '0007_marker_missing_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationcharity',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='volunteer.category'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('missing_person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteer.missingperson')),
            ],
        ),
    ]
