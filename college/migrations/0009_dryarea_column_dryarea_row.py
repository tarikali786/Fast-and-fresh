# Generated by Django 4.2.15 on 2024-08-27 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0008_filldarea_dryarea'),
    ]

    operations = [
        migrations.AddField(
            model_name='dryarea',
            name='column',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dryarea',
            name='row',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
