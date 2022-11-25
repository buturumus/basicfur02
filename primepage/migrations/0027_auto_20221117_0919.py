# Generated by Django 3.1.5 on 2022-11-17 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('primepage', '0026_auto_20221116_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyentriesbunch',
            name='cr_acc0',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_cr0', to='primepage.account'),
        ),
        migrations.AlterField(
            model_name='moneyentriesbunch',
            name='dr_acc0',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_dr0', to='primepage.account'),
        ),
        migrations.AlterField(
            model_name='moneyentriesbunch',
            name='hot_entry',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_hot_entry', to='primepage.hotentry'),
        ),
        migrations.AlterField(
            model_name='moneyentriesbunch',
            name='partner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_entry_partner', to='primepage.partner'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='hot_entry',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentry_hot_entry', to='primepage.hotentry'),
        ),
        migrations.AlterField(
            model_name='moneyentry',
            name='partner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentry_entry_partner', to='primepage.partner'),
        ),
    ]