from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.urls import reverse
import markdown


class Category(models.Model):
    '''
    分类
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    标签
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    文章的数据库表
    """
    # 文章标题
    title = models.CharField(max_length=50)

    # 文章正文
    body = models.TextField()

    # 文章的创建时间和最后一次修改时间
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now_add=True)

    # 文章摘要
    excerpt = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)

    # 分类与标签的外键定义
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章作者  从 django.contrib.auth.models 导入User
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 浏览量
    views = models.PositiveIntegerField(default=0)

    # 模型方法
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    # 默认按照时间排序
    class Meta:
        ordering = ['-created_time']

    # 获取url
    def get_absolute_url(self):
        return reverse('mysite:detail', kwargs={'id': self.pk})


# 评论模型
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]


# 资讯信息表
class D2NewsInfo(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    click = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    imgs = models.CharField(max_length=255, blank=True, null=True)
    newsurl = models.CharField(db_column='newsUrl', max_length=255, blank=True,
                               null=True)  # Field name made lowercase.
    tag = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    matchlist = models.CharField(db_column='matchList', max_length=50, blank=True,
                                 null=True)  # Field name made lowercase.
    topic_type = models.CharField(max_length=10, blank=True, null=True)
    top = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'd2_news_info'
        # 默认按照时间排序
        ordering = ['-date']

    def __str__(self):
        return self.title


class NewsInfo(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    click = models.PositiveIntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    imgs = models.CharField(max_length=255, blank=True, null=True)
    newsurl = models.CharField(db_column='newsUrl', max_length=255, blank=True,
                               null=True)  # Field name made lowercase.
    tag = models.CharField(max_length=20, blank=True, null=True)
    title = models.CharField(max_length=50, blank=True, null=True)
    top = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'news_info'
        # 默认按照时间排序
        ordering = ['-date']

    def __str__(self):
        return self.title
