# Generated by Django 3.1.5 on 2021-02-03 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_class_app', '0002_auto_20210203_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='lesson',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='my_class_app.lesson'),
        ),
    ]