from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav', 'owner')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # list_display配置列表页面展示哪些字段
    list_display = ['title', 'category', 'status', 'created_time', 'operator']

    # list_display_links配置哪些字段可以作为链接进行点击，如果为None，则不配置任何可点击的字段
    list_display_links = []

    # list_filter配置页面过滤器，需要通过哪些字段过滤页面。
    list_filter = ['category']

    # search_fields配置搜索字段
    search_fields = ['title', 'category__name']

    # actions_on_top是否展示在顶部
    actions_on_top = True

    # actions_on_bottom是否展示在底部
    actions_on_bottom = True

    # 编辑页面。 保存，编辑，编辑并新建按钮是否在顶部展示
    save_on_top = True

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj, id))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)