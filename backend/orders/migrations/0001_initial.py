# Generated by Django 4.2.16 on 2024-12-02 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('governorate', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('neighborhood', models.CharField(blank=True, max_length=100, null=True)),
                ('street', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping_address', models.CharField(blank=True, max_length=500, null=True)),
                ('purchase_count', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total_spending', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='DictionaryProductName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('session_key', models.CharField(blank=True, max_length=100, null=True)),
                ('shipping', models.FloatField(default=0)),
                ('tax', models.IntegerField(default=0)),
                ('tax_amount', models.IntegerField(default=0)),
                ('total', models.FloatField(default=0)),
                ('note', models.TextField(blank=True, null=True)),
                ('anticipation', models.CharField(blank=True, choices=[('mon', 'الاثنين'), ('tue', 'الثلاثاء'), ('wed', 'الأربعاء'), ('thu', 'الخميس'), ('fri', 'الجمعة'), ('sat', 'السبت'), ('sun', 'الأحد')], max_length=20, null=True)),
                ('tracking', models.CharField(blank=True, max_length=50, null=True)),
                ('invoice_number', models.CharField(blank=True, max_length=50, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('new', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('P', 'Placed'), ('PU', 'Pick-up'), ('Di', 'Dispatched'), ('PA', 'Package Arrived'), ('DFD', 'Dispatched for Delivery'), ('D', 'Delivery'), ('C', 'Cancel')], default='P', max_length=3)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.customers')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(blank=True, null=True, upload_to='files/images/Item/%Y/%m/%d/')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('stock_alarm', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Shipping_Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='files/images/Item/%Y/%m/%d/')),
                ('name', models.CharField(max_length=50)),
                ('shipping_price', models.FloatField(default=0)),
                ('discount_price', models.FloatField(default=0)),
                ('work_days', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='shipping_Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tax', models.IntegerField(default=0)),
                ('Shipping', models.ManyToManyField(blank=True, to='orders.shipping_company')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('date_sold', models.DateField(auto_now_add=True)),
                ('paid', models.BooleanField(default=False)),
                ('dictionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.dictionaryproductname')),
                ('notes', models.ManyToManyField(blank=True, to='cart.note')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='package',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.package'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.shipping_company'),
        ),
        migrations.AddField(
            model_name='customers',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.shipping_country'),
        ),
    ]