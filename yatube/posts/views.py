from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from .models import Post, Group, User
from .forms import PostForm


def paginate(post_list, request):
    paginator_func = Paginator(post_list, settings.NUMBER_OF_POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator_func.get_page(page_number)
    return page_obj


def index(request):
    """Передаёт в шаблон posts/index.html
    десять последних объектов модели Post."""
    post_list = Post.objects.all()
    page_obj = paginate(post_list, request)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Передаёт в шаблон posts/group_list.html
     десять последних объектов модели Post."""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = paginate(post_list, request)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    """Страница пользователя."""
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    page_obj = paginate(post_list, request)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Подробная информация о посте."""
    posts = get_object_or_404(Post, pk=post_id)
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    """Создание новых записей."""
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', request.user.username)
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request: HttpRequest, post_id: int) -> HttpRequest:
    """Редактирование имеющихся записей автора."""
    post = get_object_or_404(Post, pk=post_id)
    if post.author_id != request.user.id:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(data=request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(
        request=request,
        template_name='posts/create_post.html',
        context={'form': form, 'is_edit': True, 'post': post},
    )
