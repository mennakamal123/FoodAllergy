# Generated by Django 4.1.8 on 2023-05-14 14:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_profile_pic"),
    ]

    operations = [
        migrations.AddField(
            model_name="doctor",
            name="face_pic",
            field=models.ImageField(blank=True, null=True, upload_to="face_pic"),
        ),
    ]
