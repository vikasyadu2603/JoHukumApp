# Generated by Django 5.1.6 on 2025-03-05 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('johukumapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingslot',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
    ]
