# Generated by Django 5.1.8 on 2025-05-12 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0016_alter_customuser_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('not_completed', 'Not Completed'), ('skipped', 'Skipped')], default='not_completed', max_length=20),
        ),
        migrations.DeleteModel(
            name='Subcategory',
        ),
    ]
