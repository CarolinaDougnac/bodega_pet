# Generated by Django 4.2.2 on 2023-06-26 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bodega', '0003_import_csv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='import_csv',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]