# Generated by Django 3.1.5 on 2022-11-12 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primepage', '0018_auto_20221112_1730'),
    ]

    operations = [
        migrations.RenameField(
            model_name='killedmoneyentry',
            old_name='cred_account',
            new_name='cr_acc',
        ),
        migrations.RenameField(
            model_name='killedmoneyentry',
            old_name='deb_account',
            new_name='dr_acc',
        ),
        migrations.RenameField(
            model_name='moneyentry',
            old_name='cred_account',
            new_name='cr_acc',
        ),
        migrations.RenameField(
            model_name='moneyentry',
            old_name='deb_account',
            new_name='dr_acc',
        ),
    ]
