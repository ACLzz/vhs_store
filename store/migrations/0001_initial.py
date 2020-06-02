# Generated by Django 3.0.6 on 2020-06-01 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=90)),
                ('second_name', models.CharField(max_length=90)),
                ('birth_date', models.DateTimeField(null=True)),
                ('birth_place', models.CharField(max_length=200, null=True)),
                ('photo', models.CharField(max_length=115, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.CharField(max_length=110)),
                ('first_name', models.CharField(max_length=20)),
                ('nickname', models.CharField(max_length=25)),
                ('password', models.CharField(max_length=64)),
                ('registration_date', models.DateTimeField(auto_now=True)),
                ('birth_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=3000)),
                ('rate', models.CharField(max_length=5)),
                ('actors', models.ManyToManyField(to='store.Actor')),
                ('genres', models.ManyToManyField(to='store.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Cassette',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.CharField(max_length=125)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('film_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.Film')),
            ],
        ),
    ]
