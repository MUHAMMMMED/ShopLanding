# Generated by Django 4.2.16 on 2024-12-02 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='language',
            field=models.CharField(choices=[('ar', 'ar'), ('en', 'en')], default='ar', max_length=2),
        ),
    ]