# Generated by Django 5.1 on 2024-08-12 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_review_other_purpose_review_purpose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='phone_number',
            field=models.IntegerField(max_length=10, unique=True),
        ),
    ]
