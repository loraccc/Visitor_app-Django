# Generated by Django 5.1 on 2024-08-20 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_review_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='phone_number',
            field=models.IntegerField(max_length=10),
        ),
    ]
