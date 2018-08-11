from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import *
import logging
import markdown

# 使用定义好的日志器
logger = logging.getLogger('mysite.views')


def index(request):
    try:
        post_list = Post.objects.all()[:5]
        top_news = NewsInfo.objects.filter(top=1)[0]
        d2_top_news = D2NewsInfo.objects.filter(top=1)[0]
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['news_list'] = NewsInfo.objects.all()[:4]
        context['d2_news_list'] = D2NewsInfo.objects.all()[:4]
        context['top_news'] = NewsInfo.objects.filter(top=1)[0]
        context['d2_top_news'] = D2NewsInfo.objects.filter(top=1)[0]
        return context


def posts(request):
    try:
        post_list = Post.objects.all()
    except Exception as e:
        logger.error(e)
    return render(request, 'posts.html', locals())


# 改用通用视图
class PostsView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post_list'
    paginate_by = 8


def archives(request, year, month):
    try:
        post_list = Post.objects.filter(created_time__year=year,
                                        created_time__month=month
                                        )
    except Exception as e:
        logger.error(e)
    return render(request, 'posts.html', locals())


class ArchivesView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year,
                                                               created_time__month=month
                                                               )


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'posts.html', locals())


class CategoryView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


def detail(request, id, error_form=None):
    post = get_object_or_404(Post, id=id)
    post.increase_views()
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.toc',
                                      'markdown.extensions.codehilite',
                                  ])
    if error_form:
        form = error_form
    else:
        form = CommentForm()
    comment_list = post.comment_set.all()
    return render(request, 'detail.html', locals())


def detail_comment(request, id):
    print('收到post请求——————————')
    post = get_object_or_404(Post, id=id)
    print(post.title)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print(form)
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            print('form合法——————————')
            comment = form.save(commit=False)
            # 指定评论对应的文章
            comment.post = post
            print('拼装完成')
            comment.save()
            print('保存成功')
        else:
            return detail(request, id=id, error_form=form)
    return detail(request, id=id)


class PostDetailView(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'post'
    # 指定参数为id
    pk_url_kwarg = 'id'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 调用父类的get方法后才有object
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        # 在这里也可以增加阅读人数
        # post.increase_views()
        # 同样的方法
        # post.views = post.views + 1
        # post.save()
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class AddPostView(CreateView):
    model = Post
    fields = ['title', 'body', 'excerpt', 'category', 'tags', 'author']
    template_name = 'add.html'


def news(request):
    try:
        news_list = NewsInfo.objects.all()[:18]
        d2_news_list = D2NewsInfo.objects.all()[5:22]
        top_news_list = NewsInfo.objects.filter(top=1)[0:4]
        d2_top_news_list = D2NewsInfo.objects.all()[:4]
    except Exception as e:
        logger.error(e)
    return render(request, 'news.html', locals())
