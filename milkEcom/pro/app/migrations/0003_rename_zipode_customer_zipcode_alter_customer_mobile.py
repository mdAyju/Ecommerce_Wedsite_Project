# Generated by Django 4.2.4 on 2023-09-07 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_product_category_alter_product_product_image_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='zipode',
            new_name='zipcode',
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.IntegerField(default=0),
        ),
    ]
