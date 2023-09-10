# Generated by Django 4.2.5 on 2023-09-10 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassifiedAd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='ad_images/')),
                ('ad_type', models.CharField(choices=[('single', 'Single Item'), ('bundle', 'Bundle')], default='single', max_length=10)),
                ('bundle_items', models.TextField(blank=True)),
            ],
        ),
    ]