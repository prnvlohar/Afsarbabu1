# Generated by Django 4.2.6 on 2023-12-25 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='option1',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='option2',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='option3',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='option4',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
    ]
