# Generated by Django 3.0.6 on 2020-07-30 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Configrations', '0004_followrequestmassage_followrequests'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='followrequests',
            name='requests',
        ),
        migrations.RemoveField(
            model_name='followrequests',
            name='user',
        ),
        migrations.DeleteModel(
            name='FollowRequestMassage',
        ),
        migrations.DeleteModel(
            name='FollowRequests',
        ),
    ]