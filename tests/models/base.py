import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.template import loader
from django.template.defaulttags import register
from django.utils import timezone


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


class BaseModel(models.Model):

    def get_json(self):
        data = {}
        for field in self._meta.local_fields:
            data[field.name] = getattr(self, field.name)
        return data

    def copy_fields_from(self, model, except_fields=None):
        if except_fields is None:
            except_fields = []
        for field in model._meta.local_fields:
            if field.name not in except_fields:
                self._meta.local_fields[field.name] = getattr(model, field.name)

    def render_template(self, template, context=None):
        if context is None:
            context = {}
        return loader.get_template(template).render(context)

    class Meta:
        abstract = True


class BaseTask(BaseModel):
    name = models.CharField(max_length=50)
    number = models.IntegerField(verbose_name='Номер задания')
    title = models.TextField(default="New Task", verbose_name='Заголовок')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)

    description_md = models.TextField(default='Объяснение задания\n=======')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseTestInfo(BaseModel):
    name = models.CharField(max_length=100, default='New test', verbose_name='Название')
    description = models.TextField(default='Description', verbose_name='Описание')
    author = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    icon = models.ImageField(upload_to=user_media_path, default='test_icon.png')

    description_md = models.TextField(default='Test info\n=======')

    number_of_tasks = models.IntegerField(default=0, verbose_name='Количество заданий')

    class Meta:
        abstract = True


class BaseProject(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update(self):
        self.updated_at = timezone.now()
        self.save()

    class Meta:
        abstract = True


"""
BASE EXERCISE AND STATIC ELEMENT
"""


class BaseElement(BaseModel):
    ELEMENT_TYPES = (
        (0, 'Упражнение'),
        (1, 'Статичный элемент')
    )
    ELEMENT_PROCESSORS = {
        0: 'ProjectExercise',
        1: 'ProjectStaticElement'
    }
    element_type = models.IntegerField(choices=ELEMENT_TYPES, default=0, verbose_name='Тип элемента')

    class Meta:
        abstract = True


class BaseExercise(BaseModel):
    EXERCISE_TYPES = (
        (0, 'Ответить на вопрос'),
        (1, 'Написать развёрнутый ответ'),
        (2, 'Отметить верные утверждения'),
        (3, 'Выбрать одно верное утверждение'),
        (4, 'Соотнести что-то с чем-то'),
        (5, 'Составить правильный порядок карточек'),
        (6, 'Выбери подходящие изображения'),
    )
    EXERCISE_CLASSES = {
        0: 'AnswerExercise',
        1: 'InputExercise',
        2: 'StatementsExercise',
        3: 'RadioExercise',
        4: 'MatchExercise',
        5: 'ChronologyExercise',
        6: 'ImagesExercise'
    }
    type = models.IntegerField(choices=EXERCISE_TYPES, default=0, verbose_name='Тип упражнения')
    name = models.CharField(max_length=50, verbose_name='Название упражнения')
    title = models.CharField(max_length=150, null=True, verbose_name='Заголовок')

    exercise_id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True

    @staticmethod
    def process_request(request, exercise):
        return {}

    def render_template(self, template, context=None):
        if context is None:
            context = {}
        return super().render_template(template, {'exercise': self, **context})


class BaseStaticElement(BaseModel):
    ELEMENT_TYPES = (
        (0, 'Заголовок'),
        (1, 'Изображение'),
        (2, 'Цитата'),
        (3, 'Документ'),
        (4, 'Карты (Yandex Maps)')
    )
    ELEMENT_CLASSES = {
        0: 'TitleElement',
        1: 'PictureElement',
        2: 'QuoteElement',
        3: 'DocumentElement',
        4: 'YandexMapsElement'
    }
    type = models.IntegerField(choices=ELEMENT_TYPES, default=0, verbose_name='Тип статичного элемента')
    static_element_id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True

    @staticmethod
    def process_request(request, element):
        return {}

    def render_template(self, template, context=None):
        if context is None:
            context = {}
        return super().render_template(template, {'element': self, **context})


"""
BASE EXERCISES MODELS
"""


class BaseChronologyExercise(BaseExercise):
    type = 5

    class Meta:
        abstract = True


class BaseMatchExercise(BaseExercise):
    type = 4

    class Meta:
        abstract = True


class BaseRadioExercise(BaseExercise):
    type = 3

    class Meta:
        abstract = True


class BaseStatementsExercise(BaseExercise):
    type = 2

    class Meta:
        abstract = True


class BaseInputExercise(BaseExercise):
    type = 1

    class Meta:
        abstract = True


class BaseAnswerExercise(BaseExercise):
    type = 0

    class Meta:
        abstract = True


class BaseImagesExercise(BaseExercise):
    type = 6

    class Meta:
        abstract = True


"""
BASE ELEMENTS MODELS
"""


class BaseTitleElement(BaseStaticElement):
    title = models.TextField(default='Новый заголовок', verbose_name='Заголовок')

    class Meta:
        abstract = True


class BasePictureElement(BaseStaticElement):
    picture = models.ImageField(default='picture.jpg', verbose_name='Изображение', upload_to='project/static_pictures')

    class Meta:
        abstract = True


class BaseQuoteElement(BaseStaticElement):
    quote = models.TextField(default='Цитата - очень важный элемент для теста', verbose_name='Цитата')
    author = models.CharField(max_length=100, verbose_name='Автор цитаты')

    class Meta:
        abstract = True


class BaseDocumentElement(BaseStaticElement):
    content = models.TextField(verbose_name='Содержание документа')
    name = models.CharField(max_length=100, verbose_name='Название документа')

    class Meta:
        abstract = True


class BaseYandexMapsElement(BaseStaticElement):
    url = models.URLField()

    class Meta:
        abstract = True
