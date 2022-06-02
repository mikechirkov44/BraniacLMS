from random import choices, vonmisesvariate
from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    deleted = models.BooleanField(default=False, verbose_name="Удален")

    class Meta:
        abstract = True
        ordering = ('-created_at',)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

class NewsManager(models.Manager):

    def delete(self):
        pass

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class News(BaseModel):
    #objects = NewsManager()
    title = models.CharField(max_length=256, verbose_name="Заголовок")
    preamble = models.CharField(max_length=1024, verbose_name="Вступление")
    body = models.TextField(blank=True, null=True, verbose_name="Содержимое")
    body_as_markdown = models.BooleanField(default=False, verbose_name="Способ разметки")

    def __str__(self):
        return f"{self.pk} {self.title}"

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class Course(BaseModel):
    name = models.CharField(max_length=256, verbose_name="Наименование курса")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="Способ разметки", default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена", default=0)
    cover = models.CharField(max_length=25, default="no_image.svg", verbose_name="Обложка")

    def __str__(self):
        return f"{self.pk} {self.name}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    num = models.PositiveIntegerField(verbose_name="Номер урока")
    title = models.CharField(max_length=256, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    description_as_markdown = models.BooleanField(verbose_name="Способ разметки", default=False)

    def __str__(self):
        return f"{self.course.name} | {self.num} | {self.title}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ("course", "num",)

class CoursesTeacher(BaseModel):
    course = models.ManyToManyField(Course)
    name_first = models.CharField(max_length=128, verbose_name="Имя")
    name_second = models.CharField(max_length=128, verbose_name="Фамилия")
    day_birth = models.DateField(verbose_name="Дата рождения")

    def __str__(self):
        return "{0:0>3} {1} {2}".format(self.pk, self.name_second, self.name_first)



class CourseFeedback(BaseModel):
   
    RATINGS = (
        (5, '⭐⭐⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (3, '⭐⭐⭐'),
        (2, '⭐⭐'),
        (1, '⭐'),
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='User')
    rating = models.SmallIntegerField(choices=RATINGS, default=5, verbose_name='rating')
    feedback = models.TextField(verbose_name='Feedback', default='No Feedback')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        def __str__(self):
            return f'Отзыв на {self.course} от {self.user}'