# Generated by Django 4.2.10 on 2024-03-12 13:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_volunteer_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='created',
            field=models.CharField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
