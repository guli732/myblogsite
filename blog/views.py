from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, BlogType
from django.conf import settings


def get_blog_list_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)  # 获取页面参数
    page_of_blogs = paginator.get_page(page_num)
    currenter_page_num = page_of_blogs.number  # 获取当前页
    # 获取当前页码前后各两页的页码范围
    page_range = list(range(max(currenter_page_num - 2, 1), currenter_page_num)) + list(
        range(currenter_page_num, min(currenter_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    context = {}
    context['page_range'] = page_range
    context['blogs'] = page_of_blogs.object_list
    context['blog_types'] = BlogType.objects.all()
    context['page_of_blogs'] = page_of_blogs
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_data(request, blogs_all_list)
    return render_to_response('blog_list.html', context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, pk=blog_pk)
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()
    return render_to_response('blog_detail.html', context)


def blogs_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render_to_response('blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_data(request, blogs_all_list)
    context['blogs_with_dates'] = '%s年%s月' % (year, month)
    return render_to_response('blogs_with_date.html', context)