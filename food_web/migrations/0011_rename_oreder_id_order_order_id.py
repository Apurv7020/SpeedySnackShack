# Generated by Django 5.0.4 on 2024-05-14 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('food_web', '0010_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='oreder_id',
            new_name='order_id',
        ),
    ]