# Generated by Django 5.0.4 on 2024-05-07 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_review_rating'),
        ('store', '0009_collection_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='store.product'),
        ),
    ]
