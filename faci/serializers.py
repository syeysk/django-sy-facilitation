from django.contrib.auth import get_user_model
from rest_framework import serializers

from faci.models import FaciCanvas, ParkedThoughts, Theme, KeyThought, Expression


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


class FaciEditPreparingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaciCanvas
        fields = ['duration', 'place', 'dt_meeting', 'form_of_feedback']


class FaciAddKeyThoughtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyThought
        fields = ['key_thought', 'theme']


class FaciAddExpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expression
        fields = ['expression', 'theme', 'expression_type']


class FaciAddThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['theme', 'duration', 'description']


class FaciAddParkedThoughtsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkedThoughts
        fields = ['parked_thought']


class FaciEditAgreementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaciCanvas
        fields = ['other_agreements']
