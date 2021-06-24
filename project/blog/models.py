from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMessage
from django.db.models import *
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from taggit.managers import TaggableManager

from project import settings


class User(AbstractUser):
    email = EmailField(unique=True, verbose_name='Email')
    photo = ImageField(upload_to='users/%Y/%m/%d/', blank=True, verbose_name='Фотография')


class Category(MPTTModel):
    name = CharField(max_length=50, unique=True, verbose_name='Название')
    slug = AutoSlugField(max_length=80, populate_from='name', unique=True, always_update=True, editable=True,
                         verbose_name='URL')
    parent = TreeForeignKey('self', on_delete=PROTECT, blank=True, null=True,
                            related_name='children', verbose_name='Родительская категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-pk',)

    def save(self, *args, **kwargs):
        super(Category, self).save(**kwargs)
        Subscription.objects.get_or_create(category=self)

    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])

    def __str__(self):
        return self.name


class PublishedManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLICATION)


class Post(Model):

    class Status(TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLICATION = 'publication', 'Публикация'
        __empty__ = 'Не выбрано'

    author = ForeignKey(User, on_delete=CASCADE, related_name='posts', verbose_name='Автор')
    title = CharField(max_length=220, verbose_name='Заголовок')
    category = ForeignKey(Category, on_delete=PROTECT, null=True, related_name='posts', verbose_name='Категория')
    tags = TaggableManager(verbose_name='Теги')
    slug = AutoSlugField(max_length=255, populate_from='title', always_update=True, editable=True, verbose_name='URL')
    photo = ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True, verbose_name='Фотография')
    content = TextField(verbose_name='Наполнение')
    status = CharField(max_length=11, choices=Status.choices, default=Status.PUBLICATION, verbose_name='Статус')
    on_main_page = BooleanField(default=False, verbose_name='На главной странице')
    in_flash = BooleanField(default=False, verbose_name='В ленте')
    created = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = DateTimeField(auto_now=True, verbose_name='Дата изменения')
    published = DateTimeField(default=timezone.now, db_index=True, verbose_name='Дата публикации')
    notificated = BooleanField(default=False, verbose_name='Уведомление о посте отправлено')

    objects = Manager()
    publications = PublishedManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        unique_together = ('id', 'slug')
        ordering = ('-published',)

    def save(self, *args, **kwargs):
        super(Post, self).save(**kwargs)
        if self.status == self.Status.PUBLICATION and not self.notificated:
            self.__send_notification_to_subscribers()

    def __send_notification_to_subscribers(self):
        subscribers = self.__get_subscribers_by_post()
        mails = [subscriber.email for subscriber in subscribers]
        subject = f'Новый пост в категории {self.category}'
        message = loader.render_to_string(
            'blog/emails/notification.html',
            {
                'domain': settings.ALLOWED_HOSTS[-1],
                'category': self.category,
                'post': self,
            }
        )
        email = EmailMessage(subject, message, to=mails)
        email.content_subtype = 'html'
        email.send()
        self.__enable_post_notification_switcher()

    def __get_subscribers_by_post(self):
        return self.category.subscription.subscribers.filter(is_active=True)

    def __enable_post_notification_switcher(self):
        self.notificated = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post', args=[self.id, self.slug])

    def __str__(self):
        return self.title


class Comment(MPTTModel):

    class Status(TextChoices):
        HIDDEN = 'hidden', 'Скрыт'
        VISIBLE = 'visible', 'Виден'
        __empty__ = 'Не выбрано'

    author = ForeignKey(User, on_delete=CASCADE, related_name='comments', verbose_name='Автор')
    post = ForeignKey(Post, on_delete=CASCADE, related_name='comments', verbose_name='Пост')
    content = TextField(verbose_name='Наполнение')
    parent = TreeForeignKey('self', on_delete=CASCADE, blank=True, null=True,
                            related_name='children', verbose_name='Родительский комментарий')
    status = CharField(max_length=7, choices=Status.choices, default=Status.VISIBLE, verbose_name='Статус')
    created = DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created', 'post', 'author')

    def __str__(self):
        return f'{self.post.id}-{self.post.slug[:10]} | {self.author} / {self.content[:15]} - {str(self.created)[:-13]}'


class Subscription(Model):
    category = OneToOneField(Category, on_delete=CASCADE, related_name='subscription', verbose_name='Категория')
    subscribers = ManyToManyField(User, blank=True, related_name='subscriptions', verbose_name='Подписчики')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-category',)

    def __str__(self):
        return f'Подписка на категорию {self.category}'
