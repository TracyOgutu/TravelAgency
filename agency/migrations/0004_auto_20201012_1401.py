# Generated by Django 2.2 on 2020-10-12 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0003_reviews_review_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='review_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
