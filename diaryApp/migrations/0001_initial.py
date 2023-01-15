# Generated by Django 4.1.5 on 2023-01-14 04:28

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Main_entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_body', models.CharField(blank=True, default='Click here to type your diary entry, Also you can change the date by clicking on it.', max_length=500)),
                ('main_date', models.CharField(blank=True, max_length=50, null=True)),
                ('main_weekday', models.CharField(blank=True, max_length=50, null=True)),
                ('main_completed_tasks', models.ManyToManyField(blank=True, related_name='main_completed_tasks', to='diaryApp.task')),
                ('main_owner', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_user', to=settings.AUTH_USER_MODEL)),
                ('main_tasks', models.ManyToManyField(blank=True, null=True, related_name='main_tasks', to='diaryApp.task')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(blank=True, max_length=500)),
                ('date', models.CharField(blank=True, max_length=50, null=True)),
                ('weekday', models.CharField(blank=True, max_length=50, null=True)),
                ('completed_tasks', models.ManyToManyField(blank=True, related_name='completed_tasks', to='diaryApp.task')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('tasks', models.ManyToManyField(blank=True, null=True, related_name='tasks', to='diaryApp.task')),
            ],
        ),
        migrations.CreateModel(
            name='CompletedTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_date', models.DateTimeField(auto_now_add=True)),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diaryApp.entry')),
                ('task', models.ManyToManyField(blank=True, to='diaryApp.task')),
            ],
        ),
    ]
