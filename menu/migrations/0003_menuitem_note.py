# Generated by Django 4.0.1 on 2023-04-03 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menuitem_meal_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='note',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]