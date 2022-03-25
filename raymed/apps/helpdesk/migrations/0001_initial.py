# Generated by Django 3.2.3 on 2021-09-20 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('raymedasset', '0003_auto_20210920_1109'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Error',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_error', models.TextField(blank=True, null=True, verbose_name='Неисправность')),
                ('status', models.CharField(choices=[('wait', 'Ожидание'), ('in_work', 'В работе'), ('ready', 'Готово')], default=('wait', 'Ожидание'), max_length=30, verbose_name='Статус обращения')),
                ('post_message', models.DateTimeField(verbose_name='Время обращения')),
                ('solutions', models.TextField(blank=True, null=True, verbose_name='Решение проблемы')),
                ('device', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='raymedasset.device')),
                ('person', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
