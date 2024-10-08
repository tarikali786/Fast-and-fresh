# Generated by Django 4.2.15 on 2024-09-06 16:27

import college.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0015_alter_collection_current_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherClothBagNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_bag', models.IntegerField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to=college.models.upload_location)),
            ],
        ),
        migrations.CreateModel(
            name='OtherclothDaySheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('number_of_items', models.IntegerField(blank=True, default=0, null=True)),
                ('delivered', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='collection',
            name='completed_segregation_range',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='no_tag',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='other_cloth_campus_drop',
            field=models.ManyToManyField(blank=True, related_name='campus_drop_otherCloth_collections', to='college.otherclothbagnumber'),
        ),
        migrations.AddField(
            model_name='collection',
            name='other_cloth_campus_pickup',
            field=models.ManyToManyField(blank=True, related_name='campus_pickup_otherCloth_collections', to='college.otherclothbagnumber'),
        ),
        migrations.AddField(
            model_name='collection',
            name='other_cloth_daysheet',
            field=models.ManyToManyField(blank=True, to='college.otherclothdaysheet'),
        ),
        migrations.AddField(
            model_name='collection',
            name='other_cloth_warehouse_drop',
            field=models.ManyToManyField(blank=True, related_name='warehouse_drop_otherCloth_collections', to='college.otherclothbagnumber'),
        ),
        migrations.AddField(
            model_name='collection',
            name='other_cloth_warehouse_pickup',
            field=models.ManyToManyField(blank=True, related_name='warehouse_pickup_otherCloth_collections', to='college.otherclothbagnumber'),
        ),
    ]
