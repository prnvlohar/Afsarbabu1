# Generated by Django 4.2.9 on 2024-03-20 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0006_exams_question_images_assessment_exam'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]