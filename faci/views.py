import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django_sy_framework.linker.utils import link_instance_from_request
from faci.models import FaciCanvas, Member, KeyThought, Expression, Theme
from faci.serializers import (
    FaciEditAimSerializer,
    FaciEditMembersSerializer,
    FaciEditPreparingSerializer,
    FaciAddKeyThoughtsSerializer,
    FaciAddParkedThoughtsSerializer,
    FaciAddAgreementSerializer,
    FaciAddThemeSerializer,
    FaciAddExpressionSerializer,
)

FACI_CREATOR_FOR_WHAT = 'Инициатор встречи'


class FaciEditorView(View):
    def get(self, request, canvas_id=None):
        context = {
            'MEETING_STATUS_EDITING': FaciCanvas.MEETING_STATUS_EDITING,
            'MEETING_STATUS_STARTED': FaciCanvas.MEETING_STATUS_STARTED,
            'MEETING_STATUS_FINISHED': FaciCanvas.MEETING_STATUS_FINISHED,
            'expr_types': Expression.EXPRESSIONS_TYPES_CHOICES,
            'aim_type_choices': dict(FaciCanvas.AIM_TYPE_CHOICES),
        }

        if canvas_id:
            faci = get_object_or_404(FaciCanvas, pk=canvas_id)
            context['members'] = [
                {
                    'invited': member.invited.username,
                    'for_what': member.for_what,
                    'inviting': member.inviting.username,
                }
                for member in faci.members.all()
            ]
            context['themes'] = list(
                faci.themes.all().order_by('-dt_create').values(
                    'id', 'theme', 'duration', 'description', username=F('user__username'),
                ),
            )
            context['agreements'] = list(
                faci.agreements.all().values(
                    'id', 'agreement', 'expire_dt', 'done_dt', responsible_username=F('responsible__username'),
                )
            )
            context['has_access_to_edit_preparing'] = request.user.pk == faci.user_creator.pk
            context['has_access_to_add_members'] = request.user.is_authenticated
            context['has_access_to_edit_aim'] = request.user.pk == faci.user_creator.pk
            context['has_access_to_activate_theme'] = request.user.pk == faci.user_creator.pk
            context['has_access_to_add_key_thoughts'] = request.user.is_authenticated
            context['has_access_to_add_parked_thoughts'] = request.user.is_authenticated
            context['has_access_to_add_expression'] = request.user.is_authenticated
            context['has_access_to_add_theme'] = request.user.is_authenticated
            context['has_access_to_add_agreement'] = request.user.is_authenticated
            context['has_access_to_start_and_stop_meeting'] = request.user.pk == faci.user_creator.pk
        else:
            if not request.user.is_authenticated:
                return redirect('custom_login_page')

            faci = FaciCanvas()
            username = request.user.username
            context['members'] = [{'invited': username, 'for_what': FACI_CREATOR_FOR_WHAT, 'inviting': username}]
            context['themes'] = []
            context['agreements'] = []
            context['has_access_to_edit_preparing'] = True
            context['has_access_to_add_members'] = True
            context['has_access_to_edit_aim'] = True
            context['has_access_to_activate_theme'] = True
            context['has_access_to_add_key_thoughts'] = True
            context['has_access_to_add_parked_thoughts'] = True
            context['has_access_to_add_expression'] = True
            context['has_access_to_add_theme'] = True
            context['has_access_to_add_agreement'] = True
            context['has_access_to_start_and_stop_meeting'] = True

        context['faci'] = {
            'id': faci.pk,
            'dt_meeting': faci.dt_meeting.strftime('%Y-%m-%dT%H:%M') if faci.dt_meeting else None,
            'duration': faci.duration,
            'place': faci.place.strip(),
            'meeting_status': faci.meeting_status,
            'aim': faci.aim,
            'aim_type': faci.aim_type,
            'if_not_reached': faci.if_not_reached,
            'solutions': faci.solutions,
            'form_of_feedback': faci.form_of_feedback,
            'step': faci.step,
            'when_started': faci.when_started,
            'when_finished': faci.when_finished,
        }
        return render(request, 'faci/faci_editor.html', context)


class FaciEditAimView(APIView):
    def post(self, request, canvas_id=None):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if canvas_id:
            # Редактирование
            faci = get_object_or_404(FaciCanvas, pk=canvas_id)
            if faci.user_creator != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)

            serializer = FaciEditAimSerializer(faci, data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_fields = [
                name for name, value in serializer.validated_data.items() if getattr(faci, name) != value
            ]
            serializer.save()
        else:
            # Создание
            serializer = FaciEditAimSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            updated_fields = list(serializer.fields.keys())
            faci = serializer.save(step=FaciCanvas.STEP_MEMBERS, user_creator=request.user)
            faci.members.create(
                invited=request.user,
                inviting=request.user,
                for_what=FACI_CREATOR_FOR_WHAT,
            )
            link_instance_from_request(faci, request)

        data_for_return = {'id': faci.pk, 'step': faci.step, 'updated': updated_fields}
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class FaciEditMembersView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        serializer = FaciEditMembersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        mode = data['mode']
        invited = data['invited_user']  # TODO: обработать на фронте 400 {'unvited_username': ['пользователь не найден']}
        faci = get_object_or_404(FaciCanvas, pk=canvas_id)
        if faci.step < faci.STEP_MEMBERS:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Сначала заполните шаг {faci.STEP_AIM} (Цель)',
            )

        member = Member.objects.filter(invited=invited, faci_canvas=faci).first()
        if mode == FaciEditMembersSerializer.MODE_EDIT:
            if not member:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'invited_user': ['Пользователь не является участником встречи']},
                )

            if member.inviting.pk != request.user.pk:
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data='Запрещено редактировать приглашённого не Вами участника',
                )

            if member.for_what != data['for_what']:
                member.for_what = data['for_what']
                member.save()
        else:
            if member:
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={'invited_user': ['Пользователь уже является участником встречи']},
                )

            member = Member(invited=invited, for_what=data['for_what'], inviting=request.user, faci_canvas=faci)
            member.save()
            if faci.step == faci.STEP_MEMBERS:
                faci.step = faci.STEP_AGENDA
                faci.save()

        data_for_return = {'step': faci.step, 'success': True}
        return Response(status=status.HTTP_200_OK, data=data_for_return)

    def delete(self, canvas_id):
        ...


class FaciAddThemeView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = get_object_or_404(FaciCanvas, pk=canvas_id)
        if faci.step < faci.STEP_AGENDA:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Сначала добавьте участников',
            )

        if faci.meeting_status == faci.MEETING_STATUS_STARTED:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Встреча уже началась, добавление новых тем недоступно',
            )

        if faci.meeting_status == faci.MEETING_STATUS_FINISHED:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Встреча завершена, добавление новых тем недоступно',
            )

        serializer = FaciAddThemeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(faci=faci, user=request.user)

        if faci.step == faci.STEP_AGENDA:
            faci.step = faci.STEP_PREPARING
            faci.save()

        response_data = {
            'id': serializer.instance.id,
            'updated': list(serializer.validated_data.keys()),
            'step': faci.step,
        }
        return Response(status=status.HTTP_200_OK, data=response_data)


class FaciEditPreparingView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = get_object_or_404(FaciCanvas, pk=canvas_id)
        if faci.user_creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if faci.step < faci.STEP_PREPARING:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Сначала добавьте темы',
            )

        if faci.meeting_status == faci.MEETING_STATUS_STARTED:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Встреча уже началась, изменение подготовки недоступно',
            )

        if faci.meeting_status == faci.MEETING_STATUS_FINISHED:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Встреча завершена, изменение подготовки недоступно',
            )

        serializer = FaciEditPreparingSerializer(faci, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated = [name for name, value in serializer.validated_data.items() if getattr(faci, name) != value]
        serializer.save()
        if faci.step == faci.STEP_PREPARING:
            faci.step = faci.STEP_KEY_THOUGHTS
            faci.save()

        return Response(status=status.HTTP_200_OK, data={'step': faci.step, 'updated': updated})


class FaciStartView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = get_object_or_404(FaciCanvas, pk=canvas_id)
        if faci.user_creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if faci.step < faci.STEP_KEY_THOUGHTS:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Сначала заполните подготовку',
            )

        if faci.meeting_status == faci.MEETING_STATUS_EDITING:
            faci.meeting_status = faci.MEETING_STATUS_STARTED
            faci.when_started = datetime.datetime.now(datetime.timezone.utc)
            if faci.step == faci.STEP_KEY_THOUGHTS:
                faci.step = faci.STEP_AGREEMENTS
                faci.save()

        elif faci.meeting_status == faci.MEETING_STATUS_STARTED:
            faci.meeting_status = faci.MEETING_STATUS_FINISHED
            faci.when_finished = datetime.datetime.now(datetime.timezone.utc)
            faci.save()

        data_for_return = {
            'meeting_status': faci.meeting_status,
            'when_started': faci.when_started,
            'when_finished': faci.when_finished,
            'step': faci.step,
        }
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class FaciAddKeyThoughtsView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = get_object_or_404(FaciCanvas, pk=canvas_id)
        if faci.step < faci.STEP_AGREEMENTS:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if faci.step < faci.STEP_KEY_THOUGHTS:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Сначала заполните подготовку',
            )

        if faci.meeting_status == faci.MEETING_STATUS_EDITING:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Чтобы добавлять ключевые мысли, необходимо начать встречу',
            )

        if faci.meeting_status == faci.MEETING_STATUS_FINISHED:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Встреча завершена, добавление ключевых мыслей больше недоступно',
            )

        serializer = FaciAddKeyThoughtsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # if not faci.themes.filter(theme_id=serializer.data['theme_id']).first():
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        # theme = Theme.objects.get(theme__faci_id=canvas_id, theme_id=serializer.data['theme_id'])
        # if not theme:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        serializer.save(user=request.user)
        return Response(status=status.HTTP_200_OK, data={'updated': list(serializer.validated_data.keys())})

    # def post(self, request, canvas_id):
    #     faci = FaciCanvas.objects.get(pk=canvas_id)
    #     if not faci:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #
    #     if faci.user_creator.pk != request.user.pk:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #
    #     serializer = FaciEditKeyThoughtsSerializer(faci, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     data_for_return = {
    #         'updated': [
    #             name for name, value in serializer.validated_data.items() if getattr(faci, name) != value
    #         ],
    #     }
    #     serializer.save()
    #     return Response(status=status.HTTP_200_OK, data=data_for_return)


class FaciGetKeyThoughtsView(APIView):
    def post(self, request, canvas_id: int):
        theme_id = request.data.get('theme')
        if theme_id:
            Theme.objects.filter(faci_id=canvas_id, is_current=True).update(is_current=False)
            Theme.objects.filter(faci_id=canvas_id, pk=theme_id).update(is_current=True)
        else:
            theme = Theme.objects.filter(faci_id=canvas_id, is_current=True).first()
            if not theme:
                theme = Theme.objects.filter(faci_id=canvas_id).first()
                theme.is_current = True
                theme.save()

            theme_id = theme.pk

        key_thoughts = KeyThought.objects.filter(
            theme_id=theme_id,
            theme__faci_id=canvas_id,
        ).values('key_thought', username=F('user__username'))
        return Response(status=status.HTTP_200_OK, data={'key_thoughts': key_thoughts, 'current_theme_id': theme_id})


class FaciAddParkedThoughtsView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = get_object_or_404(FaciCanvas, pk=canvas_id)
        if faci.step < faci.STEP_KEY_THOUGHTS:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Сначала заполните подготовку',
            )

        if faci.meeting_status == faci.MEETING_STATUS_EDITING:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Чтобы парковать мысли, необходимо начать встречу',
            )

        if faci.meeting_status == faci.MEETING_STATUS_FINISHED:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Встреча завершена, паркование мыслей больше недоступно',
            )

        serializer = FaciAddParkedThoughtsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(faci=faci, user=request.user)
        return Response(status=status.HTTP_200_OK, data={'updated': list(serializer.validated_data.keys())})


class FaciGetParkedThoughtsView(APIView):
    def post(self, request, canvas_id: int):
        faci = get_object_or_404(FaciCanvas, pk=canvas_id)
        parked_thoughts = faci.parked_thoughts.all().values('parked_thought', username=F('user__username'))
        return Response(status=status.HTTP_200_OK, data={'parked_thoughts': parked_thoughts})


class FaciGetExpressionsView(APIView):
    def post(self, request, canvas_id: int):
        expressions = Expression.objects.filter(
            theme_id=request.data['theme'],
            theme__faci_id=canvas_id,
            expression_type=request.data['expression_type'],
        ).values('expression', username=F('user__username'))
        return Response(status=status.HTTP_200_OK, data={'expressions': expressions})


class FaciAddExpressionView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = get_object_or_404(FaciCanvas, pk=canvas_id)
        if faci.meeting_status == faci.MEETING_STATUS_STARTED:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Встреча уже началась, добавление недоступно',
            )

        if faci.meeting_status == faci.MEETING_STATUS_FINISHED:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Встреча завершена, добавление недоступно',
            )

        serializer = FaciAddExpressionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_200_OK, data={'updated': ['expression']})


class FaciAddAgreementView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = get_object_or_404(FaciCanvas, pk=canvas_id)
        if faci.step < faci.STEP_AGREEMENTS:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Сначала начните встречу',
            )

        if faci.meeting_status == faci.MEETING_STATUS_EDITING:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Чтобы добавлять соглашения, необходимо начать встречу',
            )

        if faci.meeting_status == faci.MEETING_STATUS_FINISHED:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data=f'Встреча завершена, добавление соглашений недоступно',
            )

        serializer = FaciAddAgreementSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(faci=faci, user=request.user)
        return Response(status=status.HTTP_200_OK, data={'id': serializer.instance.pk, 'updated': ['agreements']})


class FaciListView(View):
    def get(self, request):
        facis = (
            FaciCanvas.objects.order_by('-dt_create')
            .select_related('user_creator').prefetch_related('user_creator')
            .values('id', 'aim_type', 'aim', 'user_creator__username', 'dt_meeting')
        )

        aim_type_dict = dict(FaciCanvas.AIM_TYPE_CHOICES)
        for faci in facis:
            faci['aim_type'] = (faci['aim_type'], aim_type_dict[faci['aim_type']])

        context = {'facis': facis}
        return render(request, 'faci/faci_list.html', context)


class SearchUserView(LoginRequiredMixin, APIView):
    def post(self, request):
        search_string = request.POST['search_string']
        query = (
                    Q(username__contains=search_string)
                    | Q(last_name__contains=search_string)
                    | Q(first_name__contains=search_string)
        )
        usernames = get_user_model().objects.filter(query).values('username', 'last_name', 'first_name')[:10]
        return Response(status=status.HTTP_200_OK, data=usernames)
