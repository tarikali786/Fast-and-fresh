# Generated by Django 4.2.15 on 2024-08-27 19:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0007_logisticbagnumer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilldArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filled', models.JSONField(blank=True, null=True)),
                ('campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='college.campus')),
            ],
        ),
        migrations.CreateModel(
            name='DryArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('isActive', models.BooleanField(blank=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dry_area_id', models.IntegerField(blank=True)),
                ('fill_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='college.filldarea')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
