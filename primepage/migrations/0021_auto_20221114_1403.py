# Generated by Django 3.1.5 on 2022-11-14 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('primepage', '0020_auto_20221114_0834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hotentry',
            old_name='cr_acc',
            new_name='cr_acc0',
        ),
        migrations.RenameField(
            model_name='hotentry',
            old_name='dr_acc',
            new_name='dr_acc0',
        ),
    ]