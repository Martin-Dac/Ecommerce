# Generated by Django 4.0.5 on 2022-10-21 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_producto_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='ItemsFinal',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='orden',
            name='TotalFinal',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=13, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='descripcion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ordenitem',
            name='producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuarios.producto'),
        ),
    ]
