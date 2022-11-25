# Generated by Django 3.1.5 on 2022-11-12 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('primepage', '0017_remove_moneyentry_acc_pair'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moneyentriesbunch',
            name='acc_pairs',
        ),
        migrations.AddField(
            model_name='moneyentriesbunch',
            name='cr_acc0',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_cr0', to='primepage.account'),
        ),
        migrations.AddField(
            model_name='moneyentriesbunch',
            name='cr_acc1',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_cr1', to='primepage.account'),
        ),
        migrations.AddField(
            model_name='moneyentriesbunch',
            name='cr_acc2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_cr2', to='primepage.account'),
        ),
        migrations.AddField(
            model_name='moneyentriesbunch',
            name='dr_acc0',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_dr0', to='primepage.account'),
        ),
        migrations.AddField(
            model_name='moneyentriesbunch',
            name='dr_acc1',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_dr1', to='primepage.account'),
        ),
        migrations.AddField(
            model_name='moneyentriesbunch',
            name='dr_acc2',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='primepage_moneyentriesbunch_dr2', to='primepage.account'),
        ),
    ]