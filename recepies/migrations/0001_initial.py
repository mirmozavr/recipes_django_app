# Generated by Django 3.2.8 on 2022-03-11 12:43

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('calorie', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Recepies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
                ('text', models.CharField(max_length=500)),
                ('branch', models.CharField(choices=[('meat', 'Meat'), ('vegan', 'Vegan'), ('bakery', 'Bakery'), ('fish', 'Fish'), ('salad', 'Salad'), ('soup', 'Soup'), ('other', 'Other')], default='other', max_length=10)),
                ('slug', models.SlugField(blank=True, default='', unique=True)),
                ('cooking_time', models.DurationField(blank=True, default=datetime.timedelta(0), null=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField(default=0)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='recepies.food')),
                ('recepie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recepies.recepies')),
            ],
        ),
        migrations.AddField(
            model_name='recepies',
            name='food',
            field=models.ManyToManyField(blank=True, null=True, through='recepies.Weight', to='recepies.Food'),
        ),
    ]