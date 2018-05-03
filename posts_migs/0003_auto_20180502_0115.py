# Generated by Django 2.0.4 on 2018-05-01 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_link_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=127)),
                ('link_num', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='link',
            name='site',
            field=models.ForeignKey(default='localhost', on_delete=django.db.models.deletion.CASCADE, to='posts.Site'),
        ),
    ]
