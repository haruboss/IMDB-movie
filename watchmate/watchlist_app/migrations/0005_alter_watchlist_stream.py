# Generated by Django 5.0.7 on 2024-07-22 20:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0004_rename_stram_watchlist_stream'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='stream',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to='watchlist_app.streamplatform'),
        ),
    ]