# Generated by Django 4.0.2 on 2022-02-02 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_document_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(default=4, max_length=50),
            preserve_default=False,
        ),
    ]