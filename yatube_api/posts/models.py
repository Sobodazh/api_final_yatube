from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    slug = models.SlugField(unique=True, verbose_name='слаг')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Post(models.Model):
    text = models.TextField(verbose_name='текст')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts',
        verbose_name='автор')
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True,
        verbose_name='картинка')
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True,
        verbose_name='группа')

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='автор')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='публикация')
    text = models.TextField(verbose_name='текст')
    created = models.DateTimeField(
        auto_now_add=True, db_index=True,
        verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписчики'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='Подписки'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name="unique_user_and_following"
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
