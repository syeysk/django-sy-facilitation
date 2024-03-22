from django.contrib.auth import get_user_model
from rest_framework import serializers

from faci.models import FaciCanvas


class FaciEditAimSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaciCanvas
        fields = ['aim', 'if_not_reached', 'aim_type', 'solutions']


class AddFaciViewSerializer(serializers.Serializer):
    AIM_TYPE_CHOICES = ('solution', 'idea', 'sync')

    aim = serializers.CharField(max_length=255)
    if_not_reached = serializers.CharField(max_length=255)
    aim_type = serializers.ChoiceField(choices=AIM_TYPE_CHOICES)
    solutions = serializers.CharField(max_length=255)


class GetListFaciSerializer(serializers.Serializer):
    count_on_page = serializers.IntegerField(min_value=1, max_value=100)
    page_number = serializers.IntegerField(min_value=1)


class FaciEditMembersSerializer(serializers.Serializer):
    MODE_EDIT = 'edit'
    MODE_ADD = 'add'
    CHOICES_MODE = (
        (MODE_ADD, 'Добавление'),
        (MODE_EDIT, 'Редактирование'),
    )

    for_what = serializers.CharField(max_length=100)
    invited_user = serializers.CharField(max_length=100)
    mode = serializers.ChoiceField(choices=CHOICES_MODE)

    @staticmethod
    def validate_invited_user(value):
        value = get_user_model().objects.filter(username=value).first()
        if not value:
            raise serializers.ValidationError('Пользователя не существует')

        return value


class FaciEditAgendaSerializer(serializers.Serializer):
    themes = serializers.CharField(max_length=1000, allow_blank=True, allow_null=False)
    questions = serializers.CharField(max_length=2000, allow_blank=True, allow_null=False)
    themes_duration = serializers.IntegerField(min_value=1)
    fundamental_objections = serializers.CharField(max_length=2000, allow_blank=True, allow_null=False)
    suggested_solutions = serializers.CharField(max_length=2000, allow_blank=True, allow_null=False)
    counter_offer = serializers.CharField(max_length=2000, allow_blank=True, allow_null=False)


class FaciEditPreparingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaciCanvas
        fields = ['duration', 'place', 'dt_meeting']


class FaciEditKeyThoughtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaciCanvas
        fields = ['key_thoughts']


class FaciEditParkedThoughtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaciCanvas
        fields = ['parked_thoughts']


class FaciEditAgreementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaciCanvas
        fields = ['other_agreements']
