# Generated by Django 3.2.19 on 2023-06-06 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20230606_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='royalty',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
