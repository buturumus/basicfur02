# Generated by Django 3.1.5 on 2022-11-11 23:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('primepage', '0013_auto_20221111_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='money_entry_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='cred_account',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='money_entry_cr', to='primepage.account'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='deb_account',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='money_entry_dr', to='primepage.account'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='employee',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='money_entry_employee', to='primepage.partner'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='hot_entry',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='money_entry_hot_entry', to='primepage.hotentry'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='humanid',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='parent_money_entry',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='money_entry_parent_entry', to='primepage.moneyentry'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='partner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='money_entry_partner', to='primepage.partner'),
        ),
    ]
