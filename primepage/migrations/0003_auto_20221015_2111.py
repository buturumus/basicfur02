# Generated by Django 3.1.5 on 2022-10-15 21:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primepage', '0002_auto_20221006_1108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goodsentry',
            old_name='human_id',
            new_name='humanid',
        ),
        migrations.RenameField(
            model_name='killedgoodsentry',
            old_name='human_id',
            new_name='humanid',
        ),
        migrations.RenameField(
            model_name='killedmoneyentry',
            old_name='human_id',
            new_name='humanid',
        ),
        migrations.RenameField(
            model_name='moneyentry',
            old_name='human_id',
            new_name='humanid',
        ),
    ]