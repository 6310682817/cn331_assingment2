# Generated by Django 4.1 on 2022-10-04 14:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectData',
            fields=[
                ('sub_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('sub_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sem', models.IntegerField()),
                ('year', models.IntegerField()),
                ('seat', models.IntegerField()),
                ('max_seat', models.IntegerField()),
                ('status', models.CharField(choices=[('Open', 'Y'), ('Close', 'N')], default='Open', max_length=10)),
                ('quota_status', models.BooleanField(default=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registers_quota.subjectdata')),
            ],
            options={
                'unique_together': {('subject', 'sem', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applys', models.ManyToManyField(blank=True, related_name='stu_apply', to='registers_quota.subject')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('empty', 'empty'), ('add', 'add'), ('withdraw', 'withdraw')], default='empty', max_length=64)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registers_quota.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registers_quota.subject')),
            ],
        ),
    ]
