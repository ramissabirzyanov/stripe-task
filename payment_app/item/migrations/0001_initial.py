# Generated by Django 5.1.6 on 2025-02-26 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
                ('price', models.DecimalField(decimal_places=3, max_digits=20, verbose_name='price')),
            ],
            options={
                'verbose_name': 'Item',
                'db_table': 'Item',
                'ordering': ['id'],
            },
        ),
    ]
