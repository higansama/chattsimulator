# Generated by Django 3.2.9 on 2021-12-07 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatt', '0002_auto_20211207_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatt',
            name='rooms',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='chatt.rooms'),
            preserve_default=False,
        ),
    ]