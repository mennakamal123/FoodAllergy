# Generated by Django 4.1.8 on 2023-05-06 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="price",
        ),
        migrations.RemoveField(
            model_name="cart",
            name="product",
        ),
        migrations.RemoveField(
            model_name="cart",
            name="quantity",
        ),
        migrations.RemoveField(
            model_name="product",
            name="ratings",
        ),
        migrations.AddField(
            model_name="cart",
            name="total_price",
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.IntegerField()),
                ("price", models.FloatField(default=0)),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="cart.cart",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cart.product"
                    ),
                ),
            ],
        ),
    ]
