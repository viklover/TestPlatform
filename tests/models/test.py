import collections
import datetime
import functools
import json
import random
import operator

from django import forms
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.template import loader
from django.template.defaulttags import register
from django.utils import timezone

from tests.models.base import BaseTestInfo, BaseTask, BaseExercise, BaseModel, BaseProject, BaseElement, \
    BaseChronologyExercise, BaseMatchExercise, BaseRadioExercise, BaseStatementsExercise, BaseInputExercise, \
    BaseAnswerExercise, BaseImagesExercise, BaseStaticElement, BaseTitleElement, BasePictureElement, BaseQuoteElement, \
    BaseDocumentElement, BaseYandexMapsElement, BaseMatchListExercise


def user_media_path(instance, filename):
    return 'users/{0}/{1}'.format(instance.author.id, filename)


"""
PROJECT MODEL
"""


class Project(BaseProject, BaseTestInfo):
    project_name = models.CharField(max_length=100, verbose_name='Название проекта')
    published = models.BooleanField(default=False)

    @staticmethod
    def edit_info(form):

        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return project

        return False

    @staticmethod
    def create(form):

        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            return project

        return None

    def create_task(self, form):

        if form.is_valid():
            task = form.save(commit=False)
            task.number = self.get_tasks().count() + 1
            task.save()
            self.update()
            return task

        return None

    def create_fact(self, test_fact):

        test_fact.number_of_tasks = self.number_of_tasks
        test_fact.save()

        for task in self.get_tasks():
            task.create_fact(test_fact)

        test_fact.update_max_points()

        return test_fact

    def publish(self):

        if not self.published:
            test = Test.objects.create(project=self)
            test.copy_fields_from(self)
            test.save()

            self.published = True
            self.save()
        # else:
        #     test = Test.objects.get(project=self)

    def get_tasks(self):
        return ProjectTask.objects.filter(project=self).order_by('number')

    def get_json(self):
        return {**super().get_json(), 'number_of_tasks': self.get_tasks().count()}


class ProjectTask(BaseProject, BaseTask):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)

    def edit_info(self, form):

        if form.is_valid():
            task = form.save(commit=False)
            task.save()

            self.project.update()

    def create_exercise(self, form):

        if form.is_valid():
            exercise = form.get_exercise()
            exercise.task = self
            exercise.order = self.get_elements().count() + 1
            exercise.save()

            self.update()
            self.project.update()
            return exercise

        return None

    def create_element(self, form):

        if form.is_valid():
            element = form.get_element()
            element.task = self
            element.order = self.get_elements().count() + 1
            element.save()

            self.update()
            self.project.update()
            return element

        return None

    def create_fact(self, test_fact):

        task_fact = TaskFact().copy_fields_from(self)
        task_fact.test = test_fact
        task_fact.save()

        print(task_fact, test_fact)

        for element in self.get_elements():
            element.create_fact(task_fact)

        task_fact.update_max_points()

        return task_fact

    def get_elements(self):
        return ProjectTaskElement.objects.filter(task_id=self.id).order_by('order')

    def get_json(self):
        return {
            'number_of_exercises': ProjectTaskElement.objects.filter(task_id=self.id, element_type=0).count(),
            **super().get_json()
        }


class ProjectTaskElement(BaseProject, BaseElement):
    element_id = models.AutoField(primary_key=True, unique=True, db_column='element_id')
    task = models.ForeignKey(to=ProjectTask, on_delete=models.CASCADE, null=True)
    order = models.IntegerField(default=0, verbose_name='Порядковый номер')

    def create_fact(self, task_fact):
        return self.get_child().create_fact(task_fact)

    def get_child(self):
        return eval(f'{BaseElement.PROCESSORS[self.element_type]}.get_child_by_element(self)')

    def render(self):
        return self.render_template('editor/elements/base.html')


"""
BASE ELEMENT MODELS
"""


class ProjectExercise(ProjectTaskElement):
    EXERCISE_TYPE = -1

    id = models.AutoField(primary_key=True, unique=True)
    exercise_type = models.IntegerField(choices=BaseExercise.TYPES, default=0)

    max_points = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        self.element_type = 0
        self.exercise_type = self.EXERCISE_TYPE

        if self.exercise_type == 1:
            self.max_points = 0

        return super().save(*args, **kwargs)

    # def create_fact(self, task_fact):
    #     element = eval(f'Fact{BaseExercise.CLASSES[self.exercise_type]}()')
    #     element.task = task_fact
    #     element.order = task_fact.get_elements().count() + 1
    #     element.save()
    #
    #     return element

    def get_info(self):
        return {
            'exercise': self,
            'element': self,
            'exercise_type': BaseExercise.TYPES[self.exercise_type][1]
        }

    def create_fact(self, task_fact):
        parent = self.get_child_by_element(self)
        element = eval(f'Fact{BaseExercise.CLASSES[self.exercise_type]}().copy_fields_from(parent)')
        element.task = task_fact
        element.order = task_fact.get_elements().count() + 1
        element.save()

        print('hello', element, element.title)
        print(parent._meta.fields)

        return element

    def render(self):
        return self.render_template('editor/elements/base_exercise.html', context=self.get_info())

    @staticmethod
    def get_child_by_element(element):
        print(element, element.element_id)
        exercise_parent = ProjectExercise.objects.get(projecttaskelement_ptr_id=element.element_id)
        classname = f'Project{BaseExercise.CLASSES[exercise_parent.exercise_type]}'

        return eval(f'{classname}.objects.get(projectexercise_ptr_id={exercise_parent.id})')


class ProjectStaticElement(ProjectTaskElement):
    STATIC_ELEMENT_TYPE = -1

    id = models.AutoField(primary_key=True, unique=True)
    static_element_type = models.IntegerField(choices=BaseStaticElement.TYPES, default=0)

    def save(self, *args, **kwargs):
        self.element_type = 1
        self.static_element_type = self.STATIC_ELEMENT_TYPE
        return super().save(*args, **kwargs)

    def create_fact(self, task_fact):
        parent = self.get_child_by_element(self)
        element = eval(f'Fact{BaseStaticElement.CLASSES[self.static_element_type]}().copy_fields_from(parent)')
        element.task = task_fact
        element.order = task_fact.get_elements().count() + 1
        element.save()

        return element

    def get_info(self):
        return {
            'element': self,
            'element_type': BaseStaticElement.TYPES[self.static_element_type][1]
        }

    def render(self):
        return self.render_template('editor/elements/base_element.html', context=self.get_info())

    @staticmethod
    def get_child_by_element(element):
        element_parent = ProjectStaticElement.objects.get(projecttaskelement_ptr_id=element.element_id)
        classname = f'Project{BaseStaticElement.CLASSES[element_parent.static_element_type]}'

        return eval(f'{classname}.objects.get(projectstaticelement_ptr_id={element_parent.id})')


"""
TEST MODEL
"""


class Test(BaseModel):
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    def __render_template(self, context=None):
        if context is None:
            context = {}
        context = {
            'test': self,
            **context
        }
        template = loader.get_template('tests/test_card.html')
        return template.render(context)

    def __str__(self):
        return self.__render_template()

    def render(self, user=None):
        return self.__render_template({
            **super().get_json(),
            'user': user,
            'test_fact': TestFact.objects.filter(completed=False, user=user).last(),
            'in_progress': TestFact.objects.filter(completed=False, user=user).exists(),
            'never_opened': TestFact.objects.filter(user=user).exists()
        })

    def start(self, user):
        test_fact = TestFact(test=self, user=user)
        return self.project.create_fact(test_fact)

    def get_statistics(self, user):
        return self.__render_template(
            context={
                'with_statistics': True, 'user': user
            }
        )

    def get_statistics_differences(self, user, user_page):
        return self.__render_template(
            context={
                'with_statistics': True,
                'user': user,
                'user_res': 0.16,
                'user_page': user_page,
                'user_page_res': 0.687431
            }
        )


class TestComment(BaseModel):
    message = models.TextField(null=False)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(default=timezone.now)


class TestFact(BaseModel):
    test = models.ForeignKey(to=Test, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='Испытуемый',
                             related_name='person')

    percent = models.FloatField(default=0.0)

    max_points = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def update(self, *args, **kwargs):
        self.points = self.count_points()
        self.save()

    def update_max_points(self):
        self.max_points = 0

        for task in self.get_tasks():
            self.max_points += task.points

        self.save()

    def count_points(self):
        points = 0
        for task in self.get_tasks():
            points += task.count_points()
        return points

    @staticmethod
    def has_session(user, test_id):
        return TestFact.objects.filter(user=user, test_id=test_id, completed=False).count() != 0

    @staticmethod
    def get_session(user, test_id):
        return TestFact.objects.get(user=user, test_id=test_id, completed=False)

    @staticmethod
    def get_finished_tests(user):
        tests = []
        tests_ids = []

        facts = TestFact.objects.filter(user=user, completed=True)
        for fact in facts.order_by('percent'):
            if fact.test.id not in tests_ids:
                tests.append(fact.test)
                tests_ids.append(fact.test.id)

        return tests

    def get_tasks(self):
        return TaskFact.objects.filter(test=self).order_by('number')

    def finish(self):
        self.finished_at = datetime.datetime.now()
        self.completed = True

        self.save()


class TaskFact(BaseTask):
    test = models.ForeignKey(to=TestFact, on_delete=models.CASCADE, null=True)

    max_points = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def update(self, *args, **kwargs):
        self.points = self.count_points()
        self.save()

    def update_max_points(self):
        self.max_points = 0
        for exercise in self.get_exercises():
            self.max_points += exercise.max_points
        self.save()

    def count_points(self):
        points = 0
        for exercise in self.get_exercises():
            points += exercise.count_points()
        return points

    def get_exercises(self):
        return [obj.get_child() for obj in TaskFactElement.objects.filter(task_id=self.id, element_type=0)]

    def get_elements(self):
        return TaskFactElement.objects.filter(task_id=self.id).order_by('order')


class TaskFactElement(BaseElement):
    element_id = models.AutoField(primary_key=True, unique=True, db_column='element_id')
    task = models.ForeignKey(to=TaskFact, on_delete=models.CASCADE, null=True)
    order = models.IntegerField(default=0, verbose_name='Порядковый номер')

    def get_child(self):
        return eval(f'{BaseElement.FACT_PROCESSORS[self.element_type]}.get_child_by_element(self)')


class TestFactExercise(TaskFactElement):
    EXERCISE_TYPE = -1

    id = models.AutoField(primary_key=True, unique=True)
    exercise_type = models.IntegerField(choices=BaseExercise.TYPES, default=0)

    max_points = models.IntegerField(default=1)
    points = models.IntegerField(default=0)
    success = models.IntegerField(default=-1)

    def save(self, *args, **kwargs):
        self.element_type = 0
        self.exercise_type = self.EXERCISE_TYPE
        return super().save(*args, **kwargs)

    def finish(self):
        self.points = self.count_points()
        self.save()

    def count_points(self):
        return 0

    def prepare_exercise(self):
        return

    def process_client(self, data):
        print(self, data)
        return {}

    def render_user(self):
        return self.render_template('tests/elements/base_exercise.html')

    def get_info(self):
        return {
            'exercise': self,
            'element': self,
            'exercise_type': BaseExercise.TYPES[self.exercise_type][1]
        }

    @staticmethod
    def get_child_by_element(element):
        exercise_parent = TestFactExercise.objects.get(taskfactelement_ptr_id=element.element_id)
        classname = f'Fact{BaseExercise.CLASSES[exercise_parent.exercise_type]}'

        return eval(f'{classname}.objects.get(testfactexercise_ptr_id={exercise_parent.id})')


class TestFactStaticElement(TaskFactElement):
    STATIC_ELEMENT_TYPE = -1

    id = models.AutoField(primary_key=True, unique=True)
    static_element_type = models.IntegerField(choices=BaseStaticElement.TYPES, default=0)

    def save(self, *args, **kwargs):
        self.element_type = 1
        self.static_element_type = self.STATIC_ELEMENT_TYPE
        return super().save(*args, **kwargs)

    def get_info(self):
        return {
            'element': self,
            'element_type': BaseStaticElement.TYPES[self.static_element_type][1]
        }

    def render_user(self):
        return self.render_template('tests/elements/base_element.html', context=self.get_info())

    @staticmethod
    def get_child_by_element(element):
        element_parent = TestFactStaticElement.objects.get(taskfactelement_ptr_id=element.element_id)
        classname = f'Fact{BaseStaticElement.CLASSES[element_parent.static_element_type]}'
        return eval(f'{classname}.objects.get(testfactstaticelement_ptr_id={element_parent.id})')


"""
CHRONOLOGY EXERCISE MODEL
"""


class ChronologyExercise(BaseChronologyExercise):
    EXERCISE_TYPE = 5

    def render(self, context=None):
        if context is None:
            context = {}

        context = {
            'variants': self.get_variants(),
            **context
        }
        return self.render_template('editor/elements/chronology_exercise.html', context=context)

    @staticmethod
    def process_request(request, exercise):

        response = {'new_ids': {}}

        if 'variants' in request.POST:
            variants = json.loads(request.POST['variants'])
            order = 1

            for variant_data in variants:

                is_exist = 'id' in variant_data

                if is_exist:
                    variant = VariantChronologyExercise.objects.get(id=variant_data['id'])
                else:
                    variant = VariantChronologyExercise(exercise=exercise)

                variant.content = variant_data['content']
                variant.order = order
                variant.save()

                if not is_exist:
                    response['new_ids'][str(variant_data['test_id'])] = variant.id

                order += 1

        if 'removed_variants' in request.POST:
            variants = json.loads(request.POST['removed_variants'])

            for variant_data in variants:
                variant = VariantChronologyExercise.objects.get(id=variant_data['id'])
                variant.delete()

        return response

    def get_variants(self):
        print(self.exercise_id)
        return VariantChronologyExercise.objects.filter(exercise_id=self.exercise_id).order_by('order')


class ProjectChronologyExercise(ChronologyExercise, ProjectExercise):

    def create_fact(self, task_fact):
        chronology = super().create_fact(task_fact)

        print(chronology)

        for variant in self.get_variants():
            new_variant = VariantChronologyExercise().copy_fields_from(variant)
            new_variant.exercise = chronology
            new_variant.save()

        chronology.prepare_exercise()

        return chronology

    def render(self):
        return super().render(self.get_info())


class FactChronologyExercise(ChronologyExercise, TestFactExercise):

    def count_points(self):

        is_valid = True

        for variant in self.get_variants():
            if variant.current_order != variant.order:
                is_valid = False
                break

        return self.max_points if is_valid else 0

    def process_choice(self, request):

        if 'variants' in request.POST:
            ordering_variants = request.POST.get('variants')

            available_ids = [variant.id for variant in self.get_variants()]

            for variant_data in ordering_variants:
                if variant_data['id'] in available_ids:
                    variant = VariantChronologyExercise.objects.get(id=variant_data['id'])
                    variant.current_order = variant_data['order']
                    variant.save()

    def prepare_exercise(self):
        i = 0
        for variant in sorted(self.get_variants(), key=lambda x: random.random()):
            variant.current_order = i + 1
            variant.save()
            i += 1

    def process_client(self, data):
        print(self, data)

        variants = list(self.get_variants())

        if len(data) != len(variants):
            return {'status': False}

        variants_ids = [obj.id for obj in variants]

        for variant_id in data:
            if variant_id in variants_ids:
                variant = variants[variants_ids.index(variant_id)]
                variant.current_order = (data.index(variant_id) + 1)
                variant.save()

        return {'status': True}

    def get_variants(self):
        return super().get_variants().order_by('current_order')

    def render_user(self):
        context = {
            'variants': self.get_variants(),
            **self.get_info()
        }
        return self.render_template('tests/elements/chronology_exercise.html', context)


class VariantChronologyExercise(BaseModel):
    exercise = models.ForeignKey(to=ChronologyExercise, on_delete=models.CASCADE)
    content = models.TextField()
    order = models.IntegerField(verbose_name='Порядковый номер')
    current_order = models.IntegerField(verbose_name='Выбранный номер', default=-1)


"""
MATCH EXERCISE MODEL
"""


class MatchExercise(BaseMatchExercise):
    EXERCISE_TYPE = 4

    def render(self, context=None):
        if context is None:
            context = {}

        context = {
            'columns': self.get_columns(),
            **context
        }

        return self.render_template('editor/elements/match_exercise.html', context=context)

    @staticmethod
    def process_request(request, exercise):
        data = ColumnMatchExercise.process_request(exercise, json.loads(request.POST['data']))

        return {
            'new_ids': {
                'columns': data['columns'],
                'variants': data['variants'],
                'wrong-variants': data['wrong-variants']
            }
        }

    def get_columns(self):
        return ColumnMatchExercise.objects.filter(exercise=self)

    def get_variants(self):
        return VariantMatchExercise.objects.filter(exercise=self)

    def get_wrong_variants(self):
        return VariantMatchExercise.objects.filter(exercise=self, column=None)


class ProjectMatchExercise(MatchExercise, ProjectExercise):

    def create_fact(self, task_fact):
        match = super().create_fact(task_fact)

        columns = {
            None: None
        }

        for column in self.get_columns():
            new_column = ColumnMatchExercise().copy_fields_from(column)
            new_column.exercise = match
            new_column.save()

            columns[column.id] = new_column.id

        for variant in self.get_variants():
            new_variant = VariantMatchExercise().copy_fields_from(variant)
            new_variant.exercise = match
            new_variant.column_id = columns[variant.column_id]
            new_variant.save()

        return match

    def render(self):
        return super().render(self.get_info())


class FactMatchExercise(MatchExercise, TestFactExercise):

    def process_client(self, data):
        print(self, data)

        columns = self.get_columns()
        columns_ids = [obj.id for obj in columns]

        variants = self.get_variants()
        variants_ids = [obj.id for obj in variants]

        for column_id in data:
            if int(column_id) not in columns_ids:
                continue

            column = columns[columns_ids.index(int(column_id))]

            print(column)

            for variant_id in data[column_id]:
                if variant_id not in variants_ids:
                    continue

                variant = variants[variants_ids.index(variant_id)]
                variant.current_column = column
                variant.save()

        for variant_id in data['-1']:
            if variant_id not in variants_ids:
                continue

            variant = variants[variants_ids.index(variant_id)]
            variant.current_column = None
            variant.save()

        # variants = list(self.get_variants())
        #
        # if len(data) != len(variants):
        #     return {'status': False}
        #
        # variants_ids = [obj.id for obj in variants]
        #
        # for variant_id in data:
        #     if variant_id in variants_ids:
        #         variant = variants[variants_ids.index(variant_id)]
        #         variant.current_order = (data.index(variant_id) + 1)
        #         variant.save()

        return {'status': True}

    def get_not_chosen_variants(self):
        return VariantMatchExercise.objects.filter(current_column=None, exercise=self)

    def render_user(self):
        context = {
            'columns': self.get_columns(),
            'variants': self.get_variants(),
            **self.get_info()
        }
        return self.render_template('tests/elements/match_exercise.html', context)


class ColumnMatchExercise(BaseModel):
    exercise = models.ForeignKey(to=MatchExercise, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content

    @staticmethod
    def process_request(exercise, data):

        new_elements = {'columns': {}, 'variants': {}}

        wrong_variants_data = data['wrong-variants']
        data = data['columns']

        for column_data in data['changes']:

            is_exist = 'id' in column_data

            if is_exist:
                column = ColumnMatchExercise.objects.get(id=column_data['id'])
            else:
                column = ColumnMatchExercise(exercise=exercise)

            column.content = column_data['content']
            column.save()

            if not is_exist:
                new_elements['columns'][str(column_data['test_id'])] = column.id

            new_elements['variants'] = {
                **new_elements['variants'],
                **VariantMatchExercise.process_request(exercise, column, column_data['variants'])
            }

        for column_data in data['removed_columns']:
            columns = ColumnMatchExercise.objects.filter(id=column_data['id'])
            if columns.count():
                columns.first().delete()

        new_elements['wrong-variants'] = VariantMatchExercise.process_request(exercise, None, wrong_variants_data)

        return new_elements

    def get_current_variants(self):
        return VariantMatchExercise.objects.filter(current_column=self)

    def get_variants(self):
        return VariantMatchExercise.objects.filter(column=self)


class VariantMatchExercise(BaseModel):
    exercise = models.ForeignKey(to=MatchExercise, on_delete=models.CASCADE)
    column = models.ForeignKey(to=ColumnMatchExercise, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=100)

    current_column = models.ForeignKey(to=ColumnMatchExercise, null=True, on_delete=models.SET_NULL,
                                       related_name='current_column')

    def __str__(self):
        return self.content

    @staticmethod
    def process_request(exercise, column, data):

        new_variants = {}

        for variant_data in data['changes']:

            is_exist = 'id' in variant_data

            if is_exist:
                variant = VariantMatchExercise.objects.get(id=variant_data['id'])
            else:
                variant = VariantMatchExercise(exercise=exercise, column=column)

            variant.content = variant_data['content']
            variant.save()

            if not is_exist:
                new_variants[str(variant_data['test_id'])] = variant.id

        for variant_data in data['removed_variants']:
            variants = VariantMatchExercise.objects.filter(id=variant_data['id'])
            if variants.count():
                variants.first().delete()

        return new_variants


"""
RADIO EXERCISE MODEL
"""


class RadioExercise(BaseRadioExercise):
    EXERCISE_TYPE = 3

    def render(self, context=None):
        if context is None:
            context = {}

        context = {
            'variants': self.get_variants(),
            **context
        }
        return self.render_template('editor/elements/radio_exercise.html', context=context)

    def get_variants(self):
        return VariantRadioExercise.objects.filter(exercise=self)

    @staticmethod
    def process_request(request, exercise):

        response = {'new_ids': {}}

        if 'variants' in request.POST:
            variants = json.loads(request.POST['variants'])

            for variant_data in variants:

                is_exist = 'id' in variant_data

                if is_exist:
                    variant = VariantRadioExercise.objects.get(id=variant_data['id'])
                else:
                    variant = VariantRadioExercise(exercise=exercise)

                variant.content = variant_data['content']
                variant.is_correct = variant_data['value']
                variant.save()

                if not is_exist:
                    response['new_ids'][str(variant_data['test_id'])] = variant.id

        if 'removed_variants' in request.POST:
            variants = json.loads(request.POST['removed_variants'])

            for variant_data in variants:
                variants = VariantRadioExercise.objects.filter(id=variant_data['id'])
                if variants.count():
                    variants.first().delete()

        return response


class ProjectRadioExercise(RadioExercise, ProjectExercise):

    def create_fact(self, task_fact):
        radio = super().create_fact(task_fact)

        for variant in self.get_variants():
            new_variant = VariantRadioExercise().copy_fields_from(variant)
            new_variant.exercise = radio
            new_variant.save()

        radio.prepare_exercise()

        return radio

    def render(self):
        return super().render(self.get_info())


class FactRadioExercise(RadioExercise, TestFactExercise):

    def prepare_exercise(self):

        variants = self.get_variants()
        selected_variant = variants[random.randint(0, variants.count() - 1)]

        print('variants', variants)
        print('selected_variant', selected_variant)

        selected_variant.current_state = True
        selected_variant.save()

        print(selected_variant.current_state)

    def process_client(self, data):

        for variant in self.get_variants():
            if variant.id == data:
                variant.current_state = True
            else:
                variant.current_state = False
            variant.save()

    def render_user(self):
        context = {
            'variants': self.get_variants(),
            **self.get_info()
        }
        return self.render_template('tests/elements/radio_exercise.html', context)


class VariantRadioExercise(BaseModel):
    exercise = models.ForeignKey(to=RadioExercise, on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField(default=False)

    current_state = models.BooleanField(default=False)


"""
STATEMENTS EXERCISE MODEL
"""


class StatementsExercise(BaseStatementsExercise):
    EXERCISE_TYPE = 2

    def render(self, context=None):
        if context is None:
            context = {}

        context = {
            'variants': self.get_variants(),
            **context
        }
        return self.render_template('editor/elements/statements_exercise.html', context=context)

    def get_variants(self):
        return VariantStatementsExercise.objects.filter(exercise=self)

    @staticmethod
    def process_request(request, exercise):

        response = {'new_ids': {}}

        if 'variants' in request.POST:
            variants = json.loads(request.POST['variants'])

            for variant_data in variants:

                is_exist = 'id' in variant_data

                if is_exist:
                    variant = VariantStatementsExercise.objects.get(id=variant_data['id'])
                else:
                    variant = VariantStatementsExercise(exercise=exercise)

                variant.content = variant_data['content']
                variant.is_correct = variant_data['value']
                variant.save()

                if not is_exist:
                    response['new_ids'][str(variant_data['test_id'])] = variant.id

        if 'removed_variants' in request.POST:
            variants = json.loads(request.POST['removed_variants'])

            for variant_data in variants:
                variants = VariantStatementsExercise.objects.filter(id=variant_data['id'])
                if variants.count():
                    variants.first().delete()

        return response


class ProjectStatementsExercise(StatementsExercise, ProjectExercise):

    def create_fact(self, task_fact):
        statements = super().create_fact(task_fact)

        for variant in self.get_variants():
            new_variant = VariantStatementsExercise().copy_fields_from(variant)
            new_variant.exercise = statements
            new_variant.save()

        return statements

    def render(self):
        return super().render(self.get_info())


class FactStatementsExercise(StatementsExercise, TestFactExercise):

    def process_client(self, data):

        for variant in self.get_variants():
            if variant.id in data:
                variant.current_state = True
            else:
                variant.current_state = False
            variant.save()

    def render_user(self):
        context = {
            'variants': self.get_variants(),
            **self.get_info()
        }
        return self.render_template('tests/elements/statements_exercise.html', context)


class VariantStatementsExercise(BaseModel):
    exercise = models.ForeignKey(to=StatementsExercise, on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField(default=False)

    current_state = models.BooleanField(default=False)


"""
INPUT EXERCISE MODEL
"""


class InputExercise(BaseInputExercise):
    EXERCISE_TYPE = 1

    prepared_answer = models.TextField()

    def render(self, context=None):
        if context is None:
            context = {}
        return self.render_template('editor/elements/input_exercise.html', context=context)

    @staticmethod
    def process_request(request, exercise):
        if request.POST.get('prepared_answer', False) and request.POST.get('prepared_answer', False) != '':
            exercise.prepared_answer = request.POST.get('prepared_answer')
            exercise.save()
        return {}


class ProjectInputExercise(InputExercise, ProjectExercise):

    def create_fact(self, task_fact):
        input_exercise = super().create_fact(task_fact)
        input_exercise.prepared_answer = self.prepared_answer
        input_exercise.save()
        return input_exercise

    def render(self):
        return super().render(self.get_info())


class FactInputExercise(InputExercise, TestFactExercise):
    current_answer = models.TextField()

    def render_user(self):
        context = {
            'current_answer': self.current_answer,
            **self.get_info()
        }
        return self.render_template('tests/elements/input_exercise.html', context)

    def process_client(self, data):
        self.current_answer = data
        self.save()


"""
ANSWER EXERCISE MODEL
"""


class AnswerExercise(BaseAnswerExercise):
    EXERCISE_TYPE = 0

    correct_answer = models.TextField()

    def render(self, context=None):
        if context is None:
            context = {}
        return self.render_template('editor/elements/answer_exercise.html', context=context)

    @staticmethod
    def process_request(request, exercise):
        if request.POST.get('answer', False) and request.POST.get('answer', False) != '':
            exercise.correct_answer = request.POST.get('answer')
            exercise.save()
        return {}


class ProjectAnswerExercise(AnswerExercise, ProjectExercise):

    def create_fact(self, task_fact):
        answer = super().create_fact(task_fact)
        answer.correct_answer = self.correct_answer
        answer.save()
        return answer

    def render(self):
        return super().render(self.get_info())


class FactAnswerExercise(AnswerExercise, TestFactExercise):
    current_answer = models.TextField()

    def render_user(self):
        context = {
            'current_answer': self.current_answer,
            **self.get_info()
        }
        return self.render_template('tests/elements/answer_exercise.html', context)

    def process_client(self, data):
        self.current_answer = data
        self.save()


"""
IMAGES EXERCISE MODEL
"""


class ImagesExercise(BaseImagesExercise):
    EXERCISE_TYPE = 6

    def render(self, context=None):
        if context is None:
            context = {}

        context = {
            'pictures': self.get_pictures(),
            **context
        }
        return self.render_template('editor/elements/images_exercise.html', context=context)

    def get_pictures(self):
        return PictureImagesExercise.objects.filter(exercise=self)

    @staticmethod
    def process_request(request, exercise):

        if request.POST.get('removed_pictures', False):
            for picture_data in json.loads(request.POST['removed_pictures']):
                pictures = PictureImagesExercise.objects.filter(id=picture_data['id'])
                if pictures.count():
                    pictures.first().delete()

            return {}

        if not request.POST.get('id', False):
            form = UploadImageFrom(request.POST, request.FILES)

            if form.is_valid():
                picture = form.save(commit=False)
                picture.exercise = exercise
                picture.save()
                return {'new_id': picture.id}
            else:
                return {}

        picture = PictureImagesExercise.objects.get(id=request.POST.get('id'))
        picture.checked = True if request.POST.get('checked', 'false') == 'true' else False
        picture.save()

        return {}


class PictureImagesExercise(BaseModel):
    exercise = models.ForeignKey(to=ImagesExercise, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project/images_exercise')
    checked = models.BooleanField(default=False)

    current_checked = models.BooleanField(default=False)


class ProjectImagesExercise(ImagesExercise, ProjectExercise):

    def create_fact(self, task_fact):
        images = super().create_fact(task_fact)

        for picture in self.get_pictures():
            new_picture = PictureImagesExercise().copy_fields_from(picture)
            new_picture.exercise = images
            new_picture.save()

        return images

    def render(self):
        return super().render(self.get_info())


class FactImagesExercise(ImagesExercise, TestFactExercise):

    def render_user(self):
        context = {
            'pictures': self.get_pictures(),
            **self.get_info()
        }
        return self.render_template('tests/elements/images_exercise.html', context)

    def process_client(self, data):

        for picture in self.get_pictures():
            if picture.id in data:
                picture.current_checked = True
            else:
                picture.current_checked = False
            picture.save()


class UploadImageFrom(ModelForm):
    image = forms.ImageField()

    class Meta:
        model = PictureImagesExercise
        fields = ['image', 'checked']


"""
MATCH LIST MODEL EXERCISE 
"""


class MatchListExercise(BaseMatchListExercise):
    EXERCISE_TYPE = 7

    def render(self, context=None):
        if context is None:
            context = {}
        context = {
            'pairs': self.get_pairs(),
            **context
        }
        return self.render_template('editor/elements/matchlist_exercise.html', context=context)

    @staticmethod
    def process_request(request, exercise):

        new_elements = {'new_ids': {}}

        for key_data, value_data in json.loads(request.POST.get('pairs')):

            is_exist = 'id' in key_data

            if is_exist:
                value = ValueMatchListExercise.objects.get(id=value_data['id'])
                key = KeyMatchListExercise.objects.get(value=value)
            else:
                value = ValueMatchListExercise(exercise=exercise)
                key = KeyMatchListExercise(exercise=exercise, value=value)

            key.content = key_data['content']
            value.content = value_data['content']

            value.save()
            key.save()

            if not is_exist:
                new_elements['new_ids'][str(key_data['pair_id'])] = {}
                new_elements['new_ids'][str(key_data['pair_id'])]['key'] = key.id
                new_elements['new_ids'][str(key_data['pair_id'])]['value'] = value.id

        for key_data, value_data in json.loads(request.POST.get('removed_pairs')):
            keys = KeyMatchListExercise.objects.filter(id=key_data['id'])
            if keys.count():
                keys.first().delete()

        return new_elements

    def get_pairs(self):
        data = []
        for key in self.get_keys():
            data.append([key, key.value])
        return data

    def get_keys(self):
        return KeyMatchListExercise.objects.filter(exercise=self).order_by('order')

    def get_values(self):
        return ValueMatchListExercise.objects.filter(exercise=self)


class ProjectMatchListExercise(MatchListExercise, ProjectExercise):

    def create_fact(self, task_fact):
        matchlist = super().create_fact(task_fact)

        values = {}

        for value in self.get_values():
            new_value = ValueMatchListExercise().copy_fields_from(value)
            new_value.exercise = matchlist
            new_value.save()

            values[value.id] = new_value.id

        for key in self.get_keys():
            new_key = KeyMatchListExercise().copy_fields_from(key)
            new_key.exercise = matchlist
            new_key.value_id = values[key.value_id]
            new_key.save()

        matchlist.prepare_exercise()

        return matchlist

    def render(self):
        return super().render(self.get_info())


class FactMatchListExercise(MatchListExercise, TestFactExercise):

    def render_user(self):
        context = {
            'keys': self.get_keys(),
            'values': self.get_values(),
            **self.get_info()
        }
        return self.render_template('tests/elements/matchlist_exercise.html', context)

    def process_client(self, data):

        keys = self.get_keys()
        keys_ids = [obj.id for obj in keys]
        values_ids = [obj.id for obj in self.get_values()] + [None]

        for key_id in data:
            value_id = data[key_id]
            if value_id in values_ids and int(key_id) in keys_ids:
                key = keys[keys_ids.index(int(key_id))]
                key.set_value(value_id)

    def prepare_exercise(self):
        i = 0
        for key in sorted(self.get_keys(), key=lambda x: random.random()):
            key.order = i + 1
            key.save()
            i += 1



class ValueMatchListExercise(BaseModel):
    exercise = models.ForeignKey(to=MatchListExercise, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content


class KeyMatchListExercise(BaseModel):
    exercise = models.ForeignKey(to=MatchListExercise, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    value = models.ForeignKey(to=ValueMatchListExercise, on_delete=models.CASCADE, related_name='value')

    order = models.IntegerField(default=0)

    current_value = models.ForeignKey(to=ValueMatchListExercise, on_delete=models.CASCADE, null=True, related_name='current_value')

    def __str__(self):
        return self.content

    def set_value(self, value_id):
        if value_id is None:
            self.current_value = None
        else:
            self.current_value = ValueMatchListExercise.objects.get(id=value_id)
        self.save()

    def get_value(self):
        return self.value

    def delete(self, using=None, keep_parents=False):
        if self.value is not None:
            self.value.delete()
        super().delete(using, keep_parents)

"""
TITLE ELEMENT MODEL
"""


class TitleElement(BaseTitleElement):
    STATIC_ELEMENT_TYPE = 0

    def render(self, context=None):
        if context is None:
            context = {}
        return self.render_template('editor/elements/title_element.html', context=context)

    @staticmethod
    def process_request(request, element):
        if request.POST.get('title', False) and request.POST.get('title', False) != '':
            element.title = request.POST.get('title')
            element.save()
        return {}


class ProjectTitleElement(TitleElement, ProjectStaticElement):

    def render(self):
        return super().render(self.get_info())


class FactTitleElement(TitleElement, TestFactStaticElement):

    def render_user(self):
        context = {
            'content': self.title,
            **self.get_info()
        }
        return self.render_template('tests/elements/title_element.html', context)


"""
PICTURE ELEMENT MODEL
"""


class PictureElement(BasePictureElement):
    STATIC_ELEMENT_TYPE = 1

    def render(self, context=None):
        if context is None:
            context = {}
        return self.render_template('editor/elements/picture_element.html', context=context)

    @staticmethod
    def process_request(request, element):

        form = UploadPictureFrom(request.POST, request.FILES)

        if form.is_valid():
            picture = form.save(commit=False)
            element.picture = picture.picture
            element.save()

        return {}


class ProjectPictureElement(PictureElement, ProjectStaticElement):

    def render(self):
        return super().render(self.get_info())


class FactPictureElement(PictureElement, TestFactStaticElement):

    def render_user(self):
        context = {
            **self.get_info()
        }
        return self.render_template('tests/elements/picture_element.html', context=context)



class UploadPictureFrom(ModelForm):
    picture = forms.ImageField()

    class Meta:
        model = PictureElement
        fields = ['picture']


"""
QUOTE ELEMENT MODEL
"""


class QuoteElement(BaseQuoteElement):
    STATIC_ELEMENT_TYPE = 2

    def render(self, context=None):
        if context is None:
            context = {}
        return self.render_template('editor/elements/quote_element.html', context=context)

    @staticmethod
    def process_request(request, exercise):

        if request.POST.get('quote', False):
            exercise.quote = request.POST.get('quote')

        if request.POST.get('author', False):
            exercise.author = request.POST.get('author')

        exercise.save()
        return {}


class ProjectQuoteElement(QuoteElement, ProjectStaticElement):

    def render(self):
        return super().render(self.get_info())


class FactQuoteElement(QuoteElement, TestFactStaticElement):

    def render_user(self):
        context = {
            'content': self.quote,
            'author': self.author,
            **self.get_info()
        }
        return self.render_template('tests/elements/quote_element.html', context=context)



"""
DOCUMENT ELEMENT MODEL
"""


class DocumentElement(BaseDocumentElement):
    STATIC_ELEMENT_TYPE = 3

    def render(self, context=None):
        if context is None:
            context = {}
        return self.render_template('editor/elements/document_element.html', context=context)

    @staticmethod
    def process_request(request, exercise):

        if request.POST.get('content', False):
            exercise.content = request.POST.get('content')

        if request.POST.get('name', False):
            exercise.name = request.POST.get('name')

        exercise.save()
        return {}


class ProjectDocumentElement(DocumentElement, ProjectStaticElement):

    def render(self):
        return super().render(self.get_info())


class FactDocumentElement(DocumentElement, TestFactStaticElement):

    def render_user(self):
        context = {
            'title': self.name,
            'content': self.content,
            **self.get_info()
        }
        return self.render_template('tests/elements/document_element.html', context=context)


"""
DOCUMENT ELEMENT MODEL
"""


class YandexMapsElement(BaseYandexMapsElement):
    STATIC_ELEMENT_TYPE = 4

    def render(self, context=None):
        if context is None:
            context = {}
        return self.render_template('editor/elements/maps_element.html', context=context)

    @staticmethod
    def process_request(request, exercise):

        if request.POST.get('frame', False):
            exercise.frame = request.POST.get('frame')

        exercise.save()
        return {}


class ProjectYandexMapsElement(YandexMapsElement, ProjectStaticElement):

    def render(self):
        return super().render(self.get_info())


class FactYandexMapsElement(YandexMapsElement, TestFactStaticElement):

    def render_user(self):
        return self.render_template('tests/elements/maps_element.html', self.get_info())

