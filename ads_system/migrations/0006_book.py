# Generated by Django 4.2.5 on 2023-09-29 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads_system', '0005_alter_classifiedad_ad_type_alter_customuser_ads'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('editeur', models.CharField(max_length=200)),
                ('classe', models.CharField(max_length=200)),
                ('isbn', models.IntegerField(max_length=200)),
                ('matiere', models.CharField(max_length=200)),
            ],
        ),
    ]
