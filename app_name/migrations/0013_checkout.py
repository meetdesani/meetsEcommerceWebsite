# Generated by Django 4.2.4 on 2023-09-30 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0012_helpdesk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('statu', models.CharField(max_length=100)),
                ('zip', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('amount', models.CharField(max_length=100)),
            ],
        ),
    ]