# Generated by Django 4.1 on 2022-08-07 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0003_signup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='signup',
            options={'ordering': ['event', 'time'], 'verbose_name': 'påmelding', 'verbose_name_plural': 'påmeldinger'},
        ),
        migrations.AlterField(
            model_name='signup',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
