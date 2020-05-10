# Generated by Django 2.0.8 on 2020-05-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up', models.IntegerField(default=0, verbose_name='赞')),
                ('down', models.IntegerField(default=0, verbose_name='踩')),
                ('content', models.CharField(max_length=200, verbose_name='内容')),
                ('nickname', models.CharField(max_length=32, verbose_name='用户名')),
                ('status', models.PositiveIntegerField(choices=[(1, '正常'), (0, '删除')], default=1, verbose_name='状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '评论',
                'verbose_name_plural': '评论',
            },
        ),
    ]
