from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data, get_seven_hot_blogs
from blog.models import Blog
from django.core.cache import cache


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_read_data(blog_content_type)
    # 获取7天、今天、昨天热门博客的缓存数据
    seven_days_hot_data = cache.get('seven_days_hot_data')
    if seven_days_hot_data is None:
        seven_days_hot_data = get_seven_hot_blogs()
        cache.set('seven_days_hot_data', seven_days_hot_data, 3600)

    today_hot_data = cache.get('today_hot_data')
    if today_hot_data is None:
        today_hot_data = get_today_hot_data(blog_content_type)
        cache.set('today_hot_data', today_hot_data, 60)

    yesterday_hot_data = cache.get('yesterday_hot_data')
    if yesterday_hot_data is None:
        yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
        cache.set('yesterday_hot_data', yesterday_hot_data, 60)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['seven_days_hot_data'] = seven_days_hot_data
    return render_to_response('home.html', context)