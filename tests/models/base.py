import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import ForeignKey
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

    def deep_copy_model(self, model, updated_fk=None, related_field=None):
        child_model_relationships = []
        # Take the passed in model and get the relationships of that model
        relations = [
            f for f in model._meta.get_fields()
            if (f.one_to_many or f.one_to_one)
               and f.auto_created and not f.concrete
        ]
        # Get the list of related models for those relationships
        for relation in relations:
            accessor_name = relation.get_accessor_name()
            # Get the related field name for each relationship
            fk_field = relation.field.get_attname()
            # Build a list of child model list and related field name pairs
            child_model_relationships.append((getattr(model, accessor_name).all(), fk_field))

            # Make a copy of the model
        model.pk = None

        # If a parent model pk and related field are passed in, change that related field to the parent pk
        # if updated_fk:
        # This is what I am unable to fix.  Need to dynamically reference the models fk field to update with parent pk
        # getattr(model, related_field) = updated_fk
        # model.label_id = updated_fk
        # getattr(model, related_field) = updated_fk
        # getattr(model, related_field).SET(updated_fk)

        model.save()

        # Record the copied model's pk
        new_pk = model.pk
        # Loop through the listed pairs, deep copying each model and passing the pk and field name to update
        for child_model_relationship in child_model_relationships:
            for child_model in child_model_relationship[0]:
                self.deep_copy_model(child_model, updated_fk=new_pk, related_field=child_model_relationship[1])

        return model

    def copy_fields_from(self, model, except_fields=None):
        if except_fields is None:
            except_fields = ['id']
        # for field in model._meta.local_fields:
        for field in model._meta.fields:
            if field.name not in except_fields and 'id' not in field.name and '_ptr' not in field.name and not isinstance(field, ForeignKey):
                print(field.name)
                exec(f'self.{field.name} = getattr(model, field.name)')
                # self._meta.local_fields[field.name] = getattr(model, field.name)
        return self

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
    TYPES = (
        (0, 'Упражнение'),
        (1, 'Статичный элемент')
    )
    PROCESSORS = {
        0: 'ProjectExercise',
        1: 'ProjectStaticElement'
    }
    FACT_PROCESSORS = {
        0: 'TestFactExercise',
        1: 'TestFactStaticElement'
    }
    element_type = models.IntegerField(choices=TYPES, default=0, verbose_name='Тип элемента')

    class Meta:
        abstract = True


class BaseExercise(BaseModel):
    TYPES = (
        (0, 'Ответить на вопрос'),
        (1, 'Написать развёрнутый ответ'),
        (2, 'Отметить верные утверждения'),
        (3, 'Выбрать одно верное утверждение'),
        (4, 'Соотнести что-то с чем-то'),
        (7, 'Соотнеси что-то с элементом из списка'),
        (5, 'Составить правильный порядок карточек'),
        (6, 'Выбери подходящие изображения'),
    )
    CLASSES = {
        0: 'AnswerExercise',
        1: 'InputExercise',
        2: 'StatementsExercise',
        3: 'RadioExercise',
        4: 'MatchExercise',
        5: 'ChronologyExercise',
        6: 'ImagesExercise',
        7: 'MatchListExercise'
    }
    type = models.IntegerField(choices=TYPES, default=0, verbose_name='Тип упражнения')
    name = models.CharField(max_length=50, verbose_name='Название упражнения')
    title = models.CharField(max_length=150, null=True, verbose_name='Заголовок')

    exercise_id = models.AutoField(primary_key=True)

    EXERCISE_TYPE = -1

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.type = self.EXERCISE_TYPE
        return super().save(*args, **kwargs)

    @staticmethod
    def process_request(request, exercise):
        return {}

    def render_template(self, template, context=None):
        if context is None:
            context = {}
        return super().render_template(template, {'exercise': self, **context})


class BaseStaticElement(BaseModel):
    TYPES = (
        (0, 'Заголовок'),
        (1, 'Изображение'),
        (2, 'Цитата'),
        (3, 'Документ'),
        (4, 'Карты (Yandex Maps)')
    )
    CLASSES = {
        0: 'TitleElement',
        1: 'PictureElement',
        2: 'QuoteElement',
        3: 'DocumentElement',
        4: 'YandexMapsElement'
    }
    type = models.IntegerField(choices=TYPES, default=0, verbose_name='Тип статичного элемента')
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


class BaseMatchListExercise(BaseExercise):
    type = 7

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
    frame = models.TextField(verbose_name='iframe')

    class Meta:
        abstract = True
