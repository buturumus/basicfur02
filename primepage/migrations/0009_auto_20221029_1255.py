# Generated by Django 3.1.5 on 2022-10-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primepage', '0008_auto_20221028_2205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(max_length=256, verbose_name=''),
        ),
    ]
