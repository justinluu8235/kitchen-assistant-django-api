# Generated by Django 4.0.1 on 2022-01-27 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppinglist', '0002_pantrycategory_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pantryitem',
            name='in_stock',
            field=models.BooleanField(default=False),
        ),
    ]
