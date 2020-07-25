# Generated by Django 3.0.6 on 2020-07-25 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Configrations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bookmarked_posts', models.ManyToManyField(blank=True, to='Configrations.Post')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Configrations.Profile')),
            ],
        ),
    ]
