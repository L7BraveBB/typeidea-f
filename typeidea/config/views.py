from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import redirect

from .models import Link
from blog.views import CommonViewMixin


# Create your views here.


class LinksListView(CommonViewMixin, ListView):
    queryset = Link.objects.filter(status=Link.STATUS_NORMAL)
    template_name = 'config/links.html'
    context_object_name = 'links_list'


def links(request):
    return HttpResponse('links')
