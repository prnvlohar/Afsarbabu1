# Generated by Django 4.2.9 on 2024-03-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0004_topic_alter_assessment_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='explanation',
            field=models.CharField(max_length=2024, null=True),
        ),
    ]