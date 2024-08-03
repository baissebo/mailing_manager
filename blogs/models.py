from autoslug import AutoSlugField
from slugify import slugify
from django.db import models

from nullable import NULLABLE
from users.models import User


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name="Заголовок поста")
    slug = AutoSlugField(max_length=50, populate_from="title", unique=True, slugify=slugify)
    content = models.TextField(verbose_name="Содержимое поста")
    image = models.ImageField(upload_to="blog_images", verbose_name="Изображение", **NULLABLE
                              )
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Автор поста",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]
        permissions = [
            ("can_add_post", "Can add post"),
            ("can_change_post", "Can change post"),
            ("can_delete_post", "Can delete post")
        ]
