# Generated by Django 4.0.5 on 2022-07-21 03:28

from django.db import migrations, models
import django.db.models.query_utils


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0004_song_points_alter_player_nickname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='nickname',
            field=models.CharField(default=django.db.models.query_utils.DeferredAttribute, max_length=24),
        ),
    ]
