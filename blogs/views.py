from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blogs.forms import BlogForm, ContentManagerForm
from blogs.models import Blog


class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    paginate_by = 10
    ordering = ['-created_at']


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Blog
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blogs:blog_list')
    permission_required = 'blogs.can_add_post'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    permission_required = 'blogs.can_change_post'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title)
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogs:blog_detail', kwargs={'slug': self.object.slug})

    def get_form_class(self):
        user = self.request.user
        if user.groups.filter(name='Content manager').exists():
            return ContentManagerForm
        raise PermissionDenied


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('blogs:blog_list')
    permission_required = 'blogs.can_delete_post'
