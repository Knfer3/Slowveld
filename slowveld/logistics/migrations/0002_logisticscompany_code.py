# Generated by Django 4.0.1 on 2022-02-03 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='logisticscompany',
            name='code',
            field=models.CharField(default=1, max_length=3),
            preserve_default=False,
        ),
    ]
