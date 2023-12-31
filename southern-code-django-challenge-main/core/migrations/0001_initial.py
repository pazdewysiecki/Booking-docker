# Generated by Django 4.2.1 on 2023-07-11 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('base_price', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='PricingRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_modifier', models.FloatField(blank=True, null=True)),
                ('min_stay_length', models.IntegerField(blank=True, null=True)),
                ('fixed_price', models.FloatField(blank=True, null=True)),
                ('specific_day', models.DateField(blank=True, null=True)),
                ('properties', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.properties')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_end', models.DateField()),
                ('final_price', models.FloatField(default=0.0)),
                ('properties', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.properties')),
            ],
        ),
    ]
