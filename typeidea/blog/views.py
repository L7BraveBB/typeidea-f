from django.shortcuts import render
from django.http import HttpResponse

from .models import Tag, Post, Category
from config.models import SideBar


# Create your views here.


def post_list(request, category_id=None, tag_id=None):  # 参数是从urls.py的url中传递过来的
    tag = None
    category = None

    try:
        if tag_id:
            post_list, tag = Post.get_by_tag(tag_id)
        elif category_id:
            post_list, category = Post.get_by_category(category_id)
        else:
            post_list = Post.latest_posts()
        context = {
            'category': category,
            'tag': tag,
            'post_list': post_list,
            'sidebars': SideBar.get_all()
        }
        context.update(Category.get_navs())
        return render(request, 'blog/list.html', context=context)
    except Exception as e:
        print('post_detail view info  is error:', e)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)



