# Generated by Django 3.2 on 2022-12-13 17:24

import api.models.users
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('real_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('bio', models.TextField(default="A bio hasn't been added yet.", max_length=500)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('isDeleted', models.BooleanField(default=False)),
                ('gender', models.CharField(choices=[('O', 'Prefer Not to Say'), ('M', 'Male'), ('F', 'Female')], default='O', max_length=10)),
                ('dob', models.DateField(default=datetime.date(2000, 1, 1))),
                ('wbId', models.CharField(blank=True, max_length=150)),
                ('vxId', models.CharField(blank=True, max_length=150)),
                ('qqId', models.CharField(blank=True, max_length=150)),
                ('profile', models.ImageField(blank=True, upload_to=api.models.users.profile_to)),
                ('thumbnail', models.ImageField(blank=True, upload_to=api.models.users.thumbnail_to)),
                ('position', models.CharField(blank=True, max_length=150)),
                ('securityQuestion', models.CharField(choices=[('1', '您最喜欢的颜色？'), ('2', '您最讨厌的食物？'), ('3', '您最要好的闺蜜/兄弟？'), ('4', '您的爱好？'), ('5', '您的初恋？')], default='1', max_length=1)),
                ('securityAnswer', models.CharField(blank=True, max_length=150)),
                ('identity', models.IntegerField(choices=[(1, '普通用户'), (2, '学者')], default=0)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('scholarAuth', models.CharField(blank=True, max_length=40, null=True)),
                ('banComment', models.BooleanField(default=False)),
                ('banDuration', models.DateTimeField(blank=True, default=None, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AcademicField',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=150)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('citation', models.CharField(max_length=150)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('description', models.TextField(max_length=5000)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=150)),
                ('content', models.TextField(max_length=5000)),
                ('article', models.CharField(blank=True, max_length=40, null=True)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('atUser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='at_user', to=settings.AUTH_USER_MODEL)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review_under_review', to='api.review')),
            ],
        ),
        migrations.CreateModel(
            name='TrendSearch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('keyword', models.CharField(blank=True, max_length=150)),
                ('count', models.IntegerField()),
                ('content', models.TextField(max_length=5000)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserAuthenticateArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=40, null=True)),
                ('article_id', models.CharField(blank=True, max_length=40, null=True)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserAuthenticateScholar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(blank=True, max_length=40, null=True)),
                ('scholar_id', models.CharField(blank=True, max_length=40, null=True)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserScholar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scholar', models.CharField(blank=True, max_length=40, null=True)),
                ('scholarName', models.CharField(blank=True, max_length=150, null=True)),
                ('isFollow', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRequestScholar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(0, '已发送'), (1, '通过'), (2, '拒绝')], default=0)),
                ('unread', models.IntegerField(default=0)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('scholar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scholar', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(blank=True, max_length=150, null=True)),
                ('articleName', models.CharField(blank=True, max_length=150, null=True)),
                ('isBookmark', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Scholar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('O', 'Prefer Not to Say'), ('M', 'Male'), ('F', 'Female')], default='O', max_length=10)),
                ('dob', models.DateField(default=datetime.date(2000, 1, 1))),
                ('description', models.TextField(max_length=5000)),
                ('current_position', models.TextField(max_length=5000)),
                ('authentication_time', models.DateTimeField(blank=True, null=True)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('academicField', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.academicfield')),
                ('belongTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authenticateUser', to=settings.AUTH_USER_MODEL)),
                ('currentInstitute', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.institute')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewReport',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=5000)),
                ('category', models.IntegerField(choices=[(1, '垃圾内容'), (2, '色情内容'), (3, '非法活动'), (4, '侵犯版权'), (5, '骚扰、欺凌和威胁'), (6, '仇恨言论'), (7, '暴力内容')], default=0)),
                ('result', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('reportReview', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.review')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=5000)),
                ('reportArticle_id', models.CharField(blank=True, max_length=40, null=True)),
                ('reportScholar_id', models.CharField(blank=True, max_length=40, null=True)),
                ('category', models.IntegerField(choices=[(0, '-'), (1, '学者申诉'), (2, '学术成果申诉')], default=0)),
                ('result', models.IntegerField(choices=[(0, 'Pending'), (1, 'Reject'), (2, 'Accept')], default=0)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=5000)),
                ('scholar', models.CharField(max_length=40)),
                ('category', models.IntegerField(choices=[(0, '主问题'), (1, '提问/回复')], default=0)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('belongToQuestion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.question')),
                ('createdBy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=5000)),
                ('userId', models.CharField(blank=True, max_length=40, null=True)),
                ('userName', models.CharField(blank=True, max_length=150, null=True)),
                ('scholarId', models.CharField(blank=True, max_length=40, null=True)),
                ('scholarName', models.CharField(blank=True, max_length=150, null=True)),
                ('paperId', models.CharField(blank=True, max_length=40, null=True)),
                ('paperName', models.CharField(blank=True, max_length=150, null=True)),
                ('reviewId', models.CharField(blank=True, max_length=40, null=True)),
                ('type', models.IntegerField(choices=[(0, '无'), (1, '关注'), (2, '申诉学者接受-给用户'), (3, '申诉学者接受-给学者'), (4, '申诉学者驳回'), (5, '门户认领成功'), (6, '门户认领失败'), (7, '申诉学术成果接受-给用户'), (8, '申诉学术成果接受-给学者'), (9, '申诉学术成果失败'), (10, '评论'), (11, '回复评论'), (12, '举报评论成功 - 给评论者'), (13, '举报评论成功 - 给举报者'), (14, '举报评论驳回 - 给举报者')], default=0)),
                ('seen', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('belongTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(max_length=5000)),
                ('sentFrom', models.IntegerField(choices=[(0, '用户'), (1, '对方')], default=0)),
                ('seen', models.BooleanField(default=False)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('sentBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('userRequestScholar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userrequestscholar')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('article', models.CharField(blank=True, max_length=150, null=True)),
                ('articleName', models.CharField(blank=True, max_length=150, null=True)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('belongTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('article', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.article')),
                ('belongTo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=6)),
                ('createdAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updatedAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('sendTo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.scholar'),
        ),
    ]
