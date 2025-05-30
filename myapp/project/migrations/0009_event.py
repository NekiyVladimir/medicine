# Generated by Django 4.2.20 on 2025-05-14 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0008_alter_document_options_block_video_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название события')),
                ('description', models.TextField(blank=True, verbose_name='Описание события')),
                ('date', models.DateTimeField(verbose_name='Дата события')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Событие',
                'verbose_name_plural': 'События',
                'ordering': ['date'],
            },
        ),
    ]
