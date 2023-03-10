# Generated by Django 4.1.6 on 2023-02-06 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=256)),
                ('image', models.FileField(upload_to='')),
                ('price', models.DecimalField(decimal_places=2, max_digits=2)),
            ],
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
    ]
