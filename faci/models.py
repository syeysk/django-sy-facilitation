from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.shortcuts import resolve_url

from django_sy_framework.linker.models import Linker


class DatetimeMixin(models.Model):
    dt_create = models.DateTimeField(auto_now_add=True)
    dt_modify = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Member(models.Model):
    invited = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE, related_name='faci_members')
    inviting = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE, related_name='faci_member_inviters')
    for_what = models.CharField(verbose_name='В каком вопросе компетентен', null=False, blank=False, max_length=200)
    faci_canvas = models.ForeignKey('faci.FaciCanvas', null=False, on_delete=models.CASCADE, related_name='members')
    themes = models.CharField(  # TODO: удалить поле
        verbose_name='Тема выступления участника',
        null=False,
        default='',
        blank=True,
        max_length=1000,
    )
    themes_duration = models.IntegerField(verbose_name='Длительность выступления, минуты', null=False, default=5)
    questions = models.CharField(
        verbose_name='Вопросы',
        help_text='вопросы, возникшие касательно темы встречи',
        null=False,
        default='',
        blank=True,
        max_length=2000,
    )
    fundamental_objections = models.CharField(
        verbose_name='Принципиальные возражения',
        help_text=(
            'веские причины, отменяющие решения/предложения инициатора встречи,'
            ' делающие поставленный вопрос ничтожным'
        ),
        null=False,
        default='',
        blank=True,
        max_length=2000,
    )
    suggested_solutions = models.CharField(
        verbose_name='Предлагаемые решения',
        help_text='дополнительные предложения для решения проблемы, обозначенной инициатором встречи',
        null=False,
        default='',
        blank=True,
        max_length=2000,
    )
    counter_offer = models.CharField(
        verbose_name='Встречные предложения',
        help_text='предложение, которое заменит собой предложение инициатора встречи',
        null=False,
        default='',
        blank=True,
        max_length=2000,
    )

    class Meta:
        db_table = 'app_faci_member'
        verbose_name = 'Обязательный участник встречи'
        verbose_name_plural = 'Обязательные участники встречи'


class FaciCanvas(DatetimeMixin, models.Model):
    AIM_TYPE_SOLUTION = 1
    AIM_TYPE_IDEA = 2
    AIM_TYPE_SYNC = 3
    AIM_TYPE_OTHER = 4
    AIM_TYPE_CHOICES = (
        (AIM_TYPE_SOLUTION, 'Принять решение'),
        (AIM_TYPE_IDEA, 'Придумать идею'),
        (AIM_TYPE_SYNC, 'Синхронизироваться между собой'),
        (AIM_TYPE_OTHER, 'Прочее'),
    )

    MEETING_STATUS_EDITING = 1
    MEETING_STATUS_STARTED = 2
    MEETING_STATUS_FINISHED = 3
    MEETING_STATUS_CHOICES = (
        (MEETING_STATUS_EDITING, 'Редактируется'),
        (MEETING_STATUS_STARTED, 'Началась'),
        (MEETING_STATUS_FINISHED, 'Окончена'),
    )

    user_creator = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)
    #  1. Цель
    aim = models.CharField(verbose_name='Что мы пытаемся достичь?', max_length=255, null=False)
    if_not_reached = models.CharField(verbose_name='Что произойдёт, если цель не будет достигнута?', max_length=255, null=False)
    aim_type = models.IntegerField(verbose_name='Вид встречи', null=False, choices=AIM_TYPE_CHOICES, default=AIM_TYPE_SOLUTION)
    solutions = models.CharField(
        verbose_name='Первоначальные решения',
        max_length=255,
        null=False,
        blank=True,
        default='',
    )
    # 4. Подготовка
    dt_meeting = models.DateTimeField(verbose_name='Дата и время', null=True)
    duration = models.IntegerField(verbose_name='Длительность', null=False, default=30)
    place = models.CharField(verbose_name='Место', null=False, default='', max_length=100, blank=True)
    # 5. Ключевые мысли
    key_thoughts = models.TextField(verbose_name='Ключевые мысли', max_length=10000, null=False, default='', blank=True)
    # 6. Договорённости
    other_agreements = models.TextField(verbose_name='Прочие договорённости', max_length=10000, null=False, default='', blank=True)

    # Служебные поля
    step = models.IntegerField(verbose_name='Шаг', null=False, default=1)
    is_closed = models.IntegerField(verbose_name='Холст закрыт', null=False, default=0)
    meeting_status = models.IntegerField(verbose_name='Статус встречи', choices=MEETING_STATUS_CHOICES, default=MEETING_STATUS_EDITING, null=False, blank=False)
    linker = GenericRelation(Linker, related_query_name='faci')

    @property
    def url(self):
        return '{}{}'.format(settings.SITE_URL, resolve_url('faci_editor', self.pk))

    @property
    def url_new(self):
        return '{}{}'.format(settings.SITE_URL, resolve_url('faci_new'))

    class Meta:
        db_table = 'app_faci_canvas'
        verbose_name = 'Холст фасилитации'
        verbose_name_plural = 'Холсты фасилитации'


class ParkedThoughts(DatetimeMixin, models.Model):
    faci = models.ForeignKey('faci.FaciCanvas', null=False, on_delete=models.CASCADE, related_name="parked_thoughts")
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)
    parked_thought = models.CharField(verbose_name='Паркованная мысль', null=False, max_length=500, blank=False)

    class Meta:
        verbose_name = 'Припаркованная мысли'
        verbose_name_plural = 'Припаркованные мысли'


class Theme(DatetimeMixin, models.Model):
    faci = models.ForeignKey('faci.FaciCanvas', null=False, on_delete=models.CASCADE, related_name="themes")
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE)
    theme = models.CharField(verbose_name='Тема выступления', null=False, blank=False, max_length=1000)
    duration = models.IntegerField(verbose_name='Длительность выступления, минуты', null=False, blank=False)

    class Meta:
        verbose_name = 'Тема встречи'
        verbose_name_plural = 'Темы встречи'
