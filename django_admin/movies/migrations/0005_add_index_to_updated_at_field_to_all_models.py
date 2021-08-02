# Generated by Django 3.1 on 2021-03-30 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0004_updated_add_field_to_every_models_fix"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genre",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, db_index=True, verbose_name="Updated at"
            ),
        ),
    ]
