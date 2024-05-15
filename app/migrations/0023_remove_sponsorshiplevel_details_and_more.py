# Generated by Django 4.2.10 on 2024-05-15 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_sponsorshiplevel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sponsorshiplevel',
            name='details',
        ),
        migrations.RemoveField(
            model_name='sponsorshiplevel',
            name='price',
        ),
        migrations.AlterField(
            model_name='sponsorshiplevel',
            name='level',
            field=models.CharField(choices=[('bronze', 'Bronze Community Supporter'), ('silver', 'Silver Hope Advocate'), ('gold', 'Gold Lifesaver Leader'), ('platinum', 'Platinum Empathy Champion'), ('titanium', 'Titanium Community Ambassador')], max_length=50),
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('company', models.CharField(default='NA', max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('website_link', models.URLField(blank=True, null=True)),
                ('donation_amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('price', models.CharField(max_length=20)),
                ('details', models.TextField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sponsorshiplevel')),
            ],
        ),
    ]
