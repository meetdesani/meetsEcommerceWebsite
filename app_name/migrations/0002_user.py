# Generated by Django 4.2.4 on 2023-09-03 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_name', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=200)),
                ('lname', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=200)),
                ('mobile', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('cpassword', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('status', models.CharField(default='deactivate', max_length=200)),
            ],
        ),
    ]