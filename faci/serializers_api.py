from rest_framework import serializers


class GetListFaciSerializer(serializers.Serializer):
    count_on_page = serializers.IntegerField(min_value=1, max_value=100)
    page_number = serializers.IntegerField(min_value=1)


class AddFaciViewSerializer(serializers.Serializer):
    AIM_TYPE_CHOICES = ('solution', 'idea', 'sync')

    aim = serializers.CharField(max_length=255)
    if_not_reached = serializers.CharField(max_length=255)
    aim_type = serializers.ChoiceField(choices=AIM_TYPE_CHOICES)
    solutions = serializers.CharField(max_length=255)
