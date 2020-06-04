# Generated by Django 3.0.6 on 2020-06-04 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0006_auto_20200604_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='guide',
            name='build_jopa',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='jopa', to='firstapp.Runes'),
        ),
        migrations.AddField(
            model_name='guide',
            name='build_opa',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='opa', to='firstapp.Runes'),
        ),
    ]
