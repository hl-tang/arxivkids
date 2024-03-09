# Generated by Django 5.0.2 on 2024-02-24 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClickedPaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paper_id', models.CharField(max_length=100)),
                ('title_en', models.CharField(max_length=200)),
                ('title_ja', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('categories', models.CharField(max_length=200)),
                ('published', models.DateField()),
                ('content_en', models.TextField()),
                ('pdf_url', models.URLField()),
                ('content_ja', models.TextField()),
                ('content_plain', models.TextField()),
                ('keywords', models.TextField()),
                ('clicked_count', models.IntegerField(default=1)),
            ],
        ),
    ]