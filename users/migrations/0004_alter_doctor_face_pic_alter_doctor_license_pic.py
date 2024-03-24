# Generated by Django 4.1.8 on 2023-05-14 16:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_doctor_face_pic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="face_pic",
            field=models.ImageField(null=True, upload_to="face_pic"),
        ),
        migrations.AlterField(
            model_name="doctor",
            name="license_pic",
            field=models.ImageField(null=True, upload_to="license_pic"),
        ),
    ]
