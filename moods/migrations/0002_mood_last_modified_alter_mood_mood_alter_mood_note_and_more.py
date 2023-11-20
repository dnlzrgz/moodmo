# Generated by Django 4.2.7 on 2023-11-17 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mood',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='mood',
            name='mood',
            field=models.IntegerField(choices=[(-2, 'very unhappy'), (-1, 'unhappy'), (0, 'neutral'), (1, 'happy'), (2, 'very happy')]),
        ),
        migrations.AlterField(
            model_name='mood',
            name='note',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='mood',
            name='note_title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='mood',
            name='timestamp',
            field=models.DateTimeField(),
        ),
    ]
