# Generated by Django 4.0.1 on 2023-03-09 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0026_remove_recipe_recipe_category_recipe_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipecategory',
            name='category_name',
            field=models.CharField(default='other', max_length=50),
        ),
        migrations.AddConstraint(
            model_name='recipecategory',
            constraint=models.UniqueConstraint(fields=('user', 'category_name'), name='unique_user_category_name'),
        ),
    ]
