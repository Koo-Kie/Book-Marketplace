# Generated by Django 4.2.5 on 2023-10-06 18:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads_system', '0010_rename_editeurr_book_editeur'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='ad',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ads_system.classifiedad'),
        ),
    ]
