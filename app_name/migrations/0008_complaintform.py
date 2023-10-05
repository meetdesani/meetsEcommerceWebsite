# Generated by Django 4.2.4 on 2023-09-26 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0007_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComplaintForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brands', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('complaint', models.TextField()),
            ],
        ),
    ]