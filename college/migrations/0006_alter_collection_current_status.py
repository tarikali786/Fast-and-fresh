# Generated by Django 4.2.15 on 2024-08-27 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0005_routes_college_routes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='current_status',
            field=models.CharField(blank=True, choices=[('READY_TO_PICK', 'READY_TO_PICK'), ('IN_TRANSIT', 'IN_TRANSIT'), ('DELIVERED_TO_WAREHOUSE', 'DELIVERED_TO_WAREHOUSE'), ('WASHING', 'WASHING'), ('WASHING_DONE', 'WASHING_DONE'), ('DRYING', 'DRYING'), ('DRYING_DONE', 'DRYING_DONE'), ('IN_SEGREGATION', 'IN_SEGREGATION'), ('SEGREGATION_DONE', 'SEGREGATION_DONE'), ('READY_FOR_DELIVERY', 'READY_FOR_DELIVERY'), ('DELIVERED_TO_CAMPUS', 'DELIVERED_TO_CAMPUS'), ('DELIVERED_TO_STUDENT', 'DELIVERED_TO_STUDENT')], max_length=100, null=True),
        ),
    ]
