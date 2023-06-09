# Generated by Django 4.2 on 2023-06-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_answer_author_image_alter_answer_author_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='author_image',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='author_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='articlecomment',
            name='author_image',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='articlecomment',
            name='author_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author_image',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]