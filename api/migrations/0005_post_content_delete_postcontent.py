# Generated by Django 5.0.6 on 2024-05-31 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_postcontent_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.DeleteModel(
            name='PostContent',
        ),
    ]
