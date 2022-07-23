from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post


class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed, self).add_item_elements(handler, item)
        handler.addQuickElement('content: html', item['content_html'])


class LatestPostFeed(Feed):
    feed_type = Rss201rev2Feed  # 默认值Rss201rev2Feed，可以不写，可以自定义
    title = "Typeidea Blog System"
    link = "/rss/"
    description = "blog system power by django"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        # 用reverse时，必须在urls中加上name，根据name反向解析
        return reverse('post-detail', args=[item.pk])