# Generated by Django 5.0.1 on 2024-01-16 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_rename_sale_price_product_discount_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discount_price',
            new_name='offer_price',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='on_discount',
            new_name='on_offer',
        ),
    ]
