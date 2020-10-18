# Generated by Django 3.1.2 on 2020-10-18 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('equipment_manager', '0004_auto_20201017_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='location',
            field=models.CharField(help_text=' Location of the Equipment', max_length=20),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='vessel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='equipment_manager.vessel'),
        ),
    ]