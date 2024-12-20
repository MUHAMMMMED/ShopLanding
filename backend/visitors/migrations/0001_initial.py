# Generated by Django 4.2.16 on 2024-11-01 20:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CampaignDictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Declaration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Hour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediumDictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceDictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SourceDictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashed_ip', models.CharField(max_length=64, unique=True)),
                ('salt', models.CharField(max_length=16)),
                ('user_cookie', models.CharField(blank=True, max_length=255, null=True)),
                ('browser_fingerprint', models.CharField(blank=True, max_length=255, null=True)),
                ('user_agent', models.CharField(max_length=500)),
                ('total_visits', models.IntegerField(default=1)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_visits', to='visitors.country')),
                ('created_at', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitors.date')),
                ('device_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_visits', to='visitors.device')),
                ('operating_system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_visits', to='visitors.operatingsystem')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dictionary_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='visitors.sourcedictionary')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='visitors.country')),
                ('place_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='visitors.placedictionary')),
            ],
            options={
                'unique_together': {('place_name', 'country')},
            },
        ),
        migrations.CreateModel(
            name='Medium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dictionary_medium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='visitors.mediumdictionary')),
            ],
        ),
        migrations.CreateModel(
            name='HourlyVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaign_visits', to='visitors.campaign')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='visitors.date')),
                ('declaration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='declaration_visits', to='visitors.declaration')),
                ('hour', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hourly_visits', to='visitors.hour')),
                ('medium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medium_visits', to='visitors.medium')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_visits', to='visitors.source')),
                ('user_visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hourly_visits', to='visitors.uservisit')),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='place_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='countries', to='visitors.placedictionary'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='dictionary_campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='campaigns', to='visitors.campaigndictionary'),
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='visitors.placedictionary')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='visitors.region')),
            ],
            options={
                'unique_together': {('place_name', 'region')},
            },
        ),
    ]
