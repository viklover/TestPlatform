import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.template import loader
from django.template.defaulttags import register
from django.utils import timezone

from tests.models.base import BaseTestInfo, BaseTask, BaseExercise, BaseModel, BaseProject, BaseElement, \
    BaseChronologyExercise, BaseMatchExercise, BaseRadioExercise, BaseStatementsExercise, BaseInputExercise, \
    BaseAnswerExercise


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
            exercise.save()

            self.update()
            self.project.update()
            return exercise

        return None

    def get_json(self):
        return {
            'number_of_exercises': ProjectTaskElement.objects.filter(task_id=self.id, element_type=0).count(),
            **super().get_json()
        }


class ProjectTaskElement(BaseProject, BaseElement):
    element_id = models.AutoField(primary_key=True, unique=True, db_column='element_id')
    task = models.ForeignKey(to=ProjectTask, on_delete=models.CASCADE, null=True)

    def get_child(self):
        return eval(f'{BaseElement.ELEMENT_PROCESSORS[self.element_type]}.get_child_by_element(self)')

    def render(self):
        return self.render_template('editor/elements/base.html')


class ProjectExercise(ProjectTaskElement):
    EXERCISE_TYPE = -1

    id = models.AutoField(primary_key=True, unique=True)
    exercise_type = models.IntegerField(choices=BaseExercise.EXERCISE_TYPES, default=0)

    def save(self, *args, **kwargs):
        self.exercise_type = self.EXERCISE_TYPE
        return super().save(*args, **kwargs)

    def get_info(self):
        return {
            'exercise': self,
            'exercise_type': BaseExercise.EXERCISE_TYPES[self.exercise_type][1]
        }

    def render(self):
        return self.render_template('editor/elements/base_exercise.html', context=self.get_info())

    @staticmethod
    def get_child_by_element(element):
        exercise_parent = ProjectExercise.objects.get(projecttaskelement_ptr_id=element.element_id)
        classname = f'Project{BaseExercise.EXERCISE_CLASSES[exercise_parent.exercise_type]}'

        return eval(f'{classname}.objects.get(projectexercise_ptr_id={exercise_parent.id})')


"""
TEST MODEL
"""


class Test(BaseTestInfo):

    def __render_template(self, context=None):
        if context is None:
            context = {}
        template = loader.get_template('tests/test_card.html')
        return template.render()

    def __str__(self):
        return self.__render_template()

    def render(self, user):
        return self.__render_template({
            **super().get_json(),
            'user': user,
            'test_fact': TestFact.objects.filter(completed=False, user=user).last(),
            'in_progress': TestFact.objects.filter(completed=False, user=user).exists(),
            'never_opened': TestFact.objects.filter(user=user).exists()
        })

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


class TestFact(BaseModel):
    test = models.ForeignKey(to=Test, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(default=timezone.now)
    finished_at = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, verbose_name='Испытуемый',
                             related_name='person')

    def finish(self):
        self.finished_at = datetime.datetime.now()
        self.completed = True
        self.save()


class TestComment(BaseModel):
    message = models.TextField(null=False)
    test = models.ForeignKey(to=Test, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(), on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(default=timezone.now)


class Task(BaseTask):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    test = models.ForeignKey(to=Test, on_delete=models.SET_NULL, null=True, verbose_name='Тест')


"""
CHRONOLOGY EXERCISE MODEL
"""


class ChronologyExercise(BaseChronologyExercise):
    EXERCISE_TYPE = 5

    exercise_id = models.AutoField(primary_key=True)

    def render(self, context=None):
        if context is None:
            context = {}

        context = {
            'variants': self.get_variants(),
            **context
        }
        return self.render_template('editor/elements/chronology_exercise.html', context=context)

    def get_variants(self):
        return VariantChronologyExercise.objects.filter(exercise_id=self.id)


class ProjectChronologyExercise(ChronologyExercise, ProjectExercise):

    def render(self):
        return super().render(self.get_info())


class VariantChronologyExercise(BaseModel):
    exercise = models.ForeignKey(to=ChronologyExercise, on_delete=models.CASCADE)
    content = models.TextField()
    order = models.IntegerField(verbose_name='Порядковый номер')


"""
MATCH EXERCISE MODEL
"""


class MatchExercise(BaseMatchExercise):
    EXERCISE_TYPE = 4

    exercise_id = models.AutoField(primary_key=True)

    def get_columns(self):
        return ColumnMatchExercise.objects.filter(exercise_id=self.id)

    def get_variants(self):
        return VariantMatchExercise.objects.filter(exercise_id=self.id)


class ProjectMatchExercise(MatchExercise, ProjectExercise):
    pass


class ColumnMatchExercise(BaseModel):
    exercise = models.ForeignKey(to=MatchExercise, on_delete=models.CASCADE)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content


class VariantMatchExercise(BaseModel):
    exercise = models.ForeignKey(to=MatchExercise, on_delete=models.CASCADE)
    column = models.ForeignKey(to=ColumnMatchExercise, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.content


"""
RADIO ANSWER
"""


class RadioExercise(BaseRadioExercise):
    EXERCISE_TYPE = 3

    exercise_id = models.AutoField(primary_key=True)

    def get_variants(self):
        return VariantRadioExercise.objects.filter(exercise_id=self.id)


class ProjectRadioExercise(RadioExercise, ProjectExercise):
    pass


class VariantRadioExercise(BaseModel):
    exercise = models.ForeignKey(to=RadioExercise, on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField(default=False)


"""
STATEMENTS EXERCISE MODEL
"""


class StatementsExercise(BaseStatementsExercise):
    EXERCISE_TYPE = 2

    exercise_id = models.AutoField(primary_key=True)

    def get_variants(self):
        return VariantStatementsExercise.objects.filter(exercise_id=self.id)


class ProjectStatementsExercise(StatementsExercise, ProjectExercise):
    pass


class VariantStatementsExercise(BaseModel):
    exercise = models.ForeignKey(to=StatementsExercise, on_delete=models.CASCADE)
    content = models.TextField()
    is_correct = models.BooleanField(default=False)


"""
INPUT ANSWER
"""


class InputExercise(BaseInputExercise):
    EXERCISE_TYPE = 1

    exercise_id = models.AutoField(primary_key=True)
    prepared_answer = models.TextField()


class ProjectInputExercise(InputExercise, ProjectExercise):
    pass


"""
ANSWER ANSWER
"""


class AnswerExercise(BaseAnswerExercise):
    EXERCISE_TYPE = 0

    exercise_id = models.AutoField(primary_key=True)
    correct_answer = models.TextField()


class ProjectAnswerExercise(AnswerExercise, ProjectExercise):
    pass

