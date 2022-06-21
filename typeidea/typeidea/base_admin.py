from django.contrib import  admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. 用来自动补充文章，分类，标签，侧边栏，友联这些Model的owner字段
    2. 用queryset过滤当前用户的数据
    """

    # exclude指定哪些字段不展示, 必须是个tuple
    exclude = ('owner', )

    def get_queryset(self, request):
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)
