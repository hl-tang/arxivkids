# Generated by Django 5.0.2 on 2024-02-25 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpt_simplify', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clickedpaper',
            name='author',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='clickedpaper',
            name='categories',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='clickedpaper',
            name='paper_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='clickedpaper',
            name='published',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='clickedpaper',
            name='title_en',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='clickedpaper',
            name='title_ja',
            field=models.CharField(max_length=400),
        ),
    ]
