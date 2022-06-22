from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site
from .models import Category, Tag, Post
from .adminforms import PostAdminForm


class PostInline(admin.TabularInline):  # 可选择继承admin.StackedInline获取不同展示样式
    fields = ('title', 'desc')
    extra = 1  # 控制额外多几个
    model = Post


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav', )

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义只展示当前用户分类过滤器"""
    # 文章页面过滤器只显示当前用户创建的分类
    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')

    def queryset(self, request, queryset):
        category_id = self.value()
        print('category_id:', category_id)
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset


@admin.register(Post, site=custom_site)  # 自定义site
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    # list_display配置列表页面展示哪些字段
    list_display = ['title', 'category', 'status', 'created_time', 'operator', 'owner']

    # list_display_links配置哪些字段可以作为链接进行点击，如果为None，则不配置任何可点击的字段
    list_display_links = []

    # list_filter配置页面过滤器，需要通过哪些字段过滤页面。
    list_filter = [CategoryOwnerFilter]  # 自定义过滤条件

    # search_fields配置搜索字段
    search_fields = ['title', 'category__name']

    # actions_on_top是否展示在顶部
    actions_on_top = True

    # actions_on_bottom是否展示在底部
    actions_on_bottom = True

    # 编辑页面。 保存，编辑，编辑并新建按钮是否在顶部展示
    save_on_top = True

    # exclude指定哪些字段不展示, 必须是个tuple
    exclude = ('owner',)

    # 展示哪些字段。和页面中位置是对应的(也就是可以配置展示的顺序)
    # fields = (
    #     ('category', 'title'),
    #     'desc',
    #     'status',
    #     'content',
    #     'tag',
    # )

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag',),
        })
    )

    # 标签展示样式
    filter_horizontal = ('tag',)  # 横向展示
    # filter_vertical = ('tag',)  # 垂直展示

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    # 自定义静态资源引入，也可添加项目自身资源路径
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


@admin.register(LogEntry, site=custom_site)
class LogEntryADmin(admin.ModelAdmin ):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user',
                    'change_message']
