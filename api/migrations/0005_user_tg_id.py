# Generated by Django 5.0.2 on 2024-03-03 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_adimage_image_teleauth'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tg_id',
            field=models.BigIntegerField(null=True),
        ),
    ]
