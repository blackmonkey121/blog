# Generated by Django 2.0.8 on 2020-05-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('href', models.URLField(verbose_name='链接')),
                ('status', models.PositiveIntegerField(choices=[(1, '正常'), (0, '删除')], default=1, verbose_name='状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='收藏日期')),
            ],
            options={
                'verbose_name': '收藏表',
                'verbose_name_plural': '收藏表',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('href', models.URLField(verbose_name='链接')),
                ('status', models.PositiveIntegerField(choices=[(1, '正常'), (0, '删除')], default=1, verbose_name='状态')),
                ('weight', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, help_text='权重越高越靠前', verbose_name='权重')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '友链',
                'verbose_name_plural': '友链',
                'ordering': ['-weight'],
            },
        ),
        migrations.CreateModel(
            name='SideBar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('display_type', models.PositiveIntegerField(choices=[(1, 'HTML'), (2, '最新文章'), (3, '最热文章'), (4, '最近评论')], default=1, verbose_name='展示类型')),
                ('content', models.CharField(blank=True, help_text='如果不是HTML 可设置为空', max_length=500, verbose_name='内容')),
                ('status', models.PositiveIntegerField(choices=[(0, '隐藏'), (0, '展示')], default=1, help_text='展示或隐藏', verbose_name='状态')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '侧边栏',
                'verbose_name_plural': '侧边栏',
            },
        ),
    ]
