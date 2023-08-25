# Generated by Django 4.0.7 on 2022-08-29 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('django_celery_beat', '0016_alter_crontabschedule_timezone'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, verbose_name='标题')),
                ('link', models.CharField(blank=True, max_length=256, verbose_name='链接')),
                ('content', models.CharField(blank=True, max_length=256, verbose_name='描述')),
                ('icon', models.CharField(blank=True, max_length=256, null=True, verbose_name='图标')),
                ('is_piracy', models.BooleanField(default=False, verbose_name='盗版标识符')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='创建日期')),
            ],
            options={
                'verbose_name': '渠道爬取信息',
                'ordering': ['source_state_id'],
            },
        ),
        migrations.CreateModel(
            name='ScheduledModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(blank=True, max_length=128, verbose_name='关键词')),
                ('sources_list', models.CharField(blank=True, max_length=256, verbose_name='渠道清单')),
                ('schedule', models.DecimalField(decimal_places=1, max_digits=5, verbose_name='定时')),
                ('state', models.SmallIntegerField(choices=[(0, 'Error'), (1, 'Start'), (2, 'Unstart')], verbose_name='状态')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='创建日期')),
            ],
        ),
        migrations.CreateModel(
            name='StateModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(default='', max_length=32, verbose_name='job任务标识')),
                ('date', models.DateTimeField(verbose_name='创建日期')),
                ('keyword', models.CharField(max_length=20, verbose_name='关键字')),
                ('source', models.CharField(max_length=20, verbose_name='渠道')),
                ('state', models.SmallIntegerField(choices=[(0, 'Killed'), (1, 'Running'), (2, 'Finished')], verbose_name='状态')),
            ],
            options={
                'verbose_name': '爬取状态',
                'verbose_name_plural': '爬取状态',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='邮箱', max_length=254, unique=True, verbose_name='邮箱')),
                ('name', models.CharField(help_text='名字', max_length=128, verbose_name='名字')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.AddIndex(
            model_name='usermodel',
            index=models.Index(fields=['email'], name='inspection__email_f55d32_idx'),
        ),
        migrations.AddField(
            model_name='statemodel',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection.usermodel', verbose_name='所有者'),
        ),
        migrations.AddField(
            model_name='scheduledmodel',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection.usermodel', verbose_name='所有者'),
        ),
        migrations.AddField(
            model_name='scheduledmodel',
            name='periodic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.periodictask', verbose_name='任务外键'),
        ),
        migrations.AddField(
            model_name='infomodel',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection.usermodel', verbose_name='所有者'),
        ),
        migrations.AddField(
            model_name='infomodel',
            name='source_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection.statemodel', verbose_name='爬取源'),
        ),
    ]