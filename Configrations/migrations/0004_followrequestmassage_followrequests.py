# Generated by Django 3.0.6 on 2020-07-29 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Configrations', '0003_auto_20200724_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowRequestMassage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('SEND', 'SEND'), ('REGECTED', 'REGECTED'), ('ACCEPTED', 'ACCEPTED')], max_length=10, null=True)),
                ('user_acted_on', models.DateTimeField(blank=True)),
                ('send_on', models.DateTimeField(auto_now_add=True)),
                ('send_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('send_to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Configrations.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='FollowRequests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requests', models.ManyToManyField(to='Configrations.FollowRequestMassage')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Configrations.Profile')),
            ],
        ),
    ]
