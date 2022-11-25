# Generated by Django 3.1.5 on 2022-11-12 13:02

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import misc.common_classes
import primepage.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('primepage', '0014_auto_20221111_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyentry',
            name='comment',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0)),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='created_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentry_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='employee',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentry_employee', to='primepage.partner'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='hot_entry',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentry_hot_entry', to='primepage.hotentry'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='money',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='parent_money_entry',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentry_parent_entry', to='primepage.moneyentry'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='partner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentry_entry_partner', to='primepage.partner'),
        ),
        migrations.CreateModel(
            name='MoneyEntriesBunch',
            fields=[
                ('humanid', models.CharField(blank=True, default='', max_length=32)),
                ('money', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('date', models.DateField()),
                ('comment', models.CharField(blank=True, max_length=256)),
                ('create_date', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0))),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_created_by', to=settings.AUTH_USER_MODEL)),
                ('cred_account', models.ManyToManyField(related_name='primepage_moneyentriesbunch_crs', to='primepage.Account')),
                ('deb_accounts', models.ManyToManyField(related_name='primepage_moneyentriesbunch_drs', to='primepage.Account')),
                ('employee', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_employee', to='primepage.partner')),
                ('hot_entry', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_hot_entry', to='primepage.hotentry')),
                ('parent_money_entry', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_parent_entry', to='primepage.moneyentriesbunch')),
                ('partner', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_entry_partner', to='primepage.partner')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, misc.common_classes.ClassNameGetter, primepage.models.SaveDataKeeper),
        ),
    ]