# Generated by Django 2.2 on 2020-09-27 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countryname', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custname', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destname', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=30)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency.Country')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('packagename', models.CharField(max_length=30)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('description', models.CharField(max_length=100)),
                ('duration', models.IntegerField(default=1)),
                ('dest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency.Destination')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency.Customer')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency.Destination')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agency.Package')),
            ],
        ),
    ]
