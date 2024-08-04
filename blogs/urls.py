from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from blogs.apps import BlogsConfig
from blogs.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = BlogsConfig.name

urlpatterns = [
    path('blog-list/', cache_page(60 * 10)(BlogListView.as_view()), name='blog_list'),
    path('blog/<slug:slug>/', cache_page(60 * 15)(BlogDetailView.as_view()), name='blog_detail'),
    path('create-blog/', BlogCreateView.as_view(), name='blog_create'),
    path('update-blog/<slug:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('delete-blog/<slug:slug>/', BlogDeleteView.as_view(), name='blog_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
