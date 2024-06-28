# Generated by Django 5.0.6 on 2024-06-25 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0003_createcode_color_code_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='colorcode',
            name='material_group',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='createcode',
            name='color_code_choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='color_code_choice', to='cal.colorcode', verbose_name='Color Code:'),
        ),
    ]