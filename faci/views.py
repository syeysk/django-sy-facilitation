from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django_sy_framework.linker.utils import link_instance_from_request
from faci.models import FaciCanvas, Member, KeyThought, Expression, Theme
from faci.serializers import (
    AddFaciViewSerializer,
    GetListFaciSerializer,
    FaciEditAimSerializer,
    FaciEditMembersSerializer,
    FaciEditPreparingSerializer,
    FaciAddKeyThoughtsSerializer,
    FaciAddParkedThoughtsSerializer,
    FaciEditAgreementsSerializer,
    FaciAddThemeSerializer,
    FaciAddExpressionSerializer,
)

FACI_CREATOR_FOR_WHAT = 'Инициатор встречи'


class FaciEditorView(View):
    def get(self, request, canvas_id=None):
        if canvas_id:
            faci = get_object_or_404(FaciCanvas, pk=canvas_id)
            step = faci.step
            members = [
                {
                    'invited': member.invited.username,
                    'for_what': member.for_what,
                    'inviting': member.inviting.username,
                }
                for member in faci.members.all()
            ]
            themes = list(
                faci.themes.all().order_by('-dt_create').values(
                    'id', 'theme', 'duration', 'description', username=F('user__username'),
                ),
            )
            has_access_to_edit_preparing = request.user.pk == faci.user_creator.pk
            has_access_to_add_members = request.user.is_authenticated
            has_access_to_edit_aim = request.user.pk == faci.user_creator.pk
            has_access_to_activate_theme = request.user.pk == faci.user_creator.pk
            has_access_to_add_key_thoughts = request.user.is_authenticated
            has_access_to_add_parked_thoughts = request.user.is_authenticated
            has_access_to_add_expression = request.user.is_authenticated
            has_access_to_add_theme = request.user.is_authenticated
        else:
            if not request.user.is_authenticated:
                return redirect('custom_login_page')

            faci = FaciCanvas()
            step = 1
            username = request.user.username
            members = [{'invited': username, 'for_what': FACI_CREATOR_FOR_WHAT, 'inviting': username}]
            themes = []
            has_access_to_edit_preparing = True
            has_access_to_add_members = True
            has_access_to_edit_aim = True
            has_access_to_activate_theme = True
            has_access_to_add_key_thoughts = True
            has_access_to_add_parked_thoughts = True
            has_access_to_add_expression = True
            has_access_to_add_theme = True

        context = {
            'faci': faci,
            'faci_json': {
                'dt_meeting': faci.dt_meeting.strftime('%Y-%m-%dT%H:%M') if faci.dt_meeting else None,
                'duration': faci.duration,
                'place': faci.place.strip(),
                'meeting_status': faci.meeting_status,
                'aim': faci.aim,
                'aim_type': faci.aim_type,
                'if_not_reached': faci.if_not_reached,
                'solutions': faci.solutions,
                'other_agreements': faci.other_agreements,
                'form_of_feedback': faci.form_of_feedback,
            },
            'themes': themes,
            'expr_types': Expression.EXPRESSIONS_TYPES_CHOICES,
            'aim_type_choices': dict(FaciCanvas.AIM_TYPE_CHOICES),
            'step': step,
            'members': members,
            'has_access_to_edit_preparing': has_access_to_edit_preparing,
            'has_access_to_add_members': has_access_to_add_members,
            'has_access_to_edit_aim': has_access_to_edit_aim,
            'has_access_to_activate_theme': has_access_to_activate_theme,
            'has_access_to_add_key_thoughts': has_access_to_add_key_thoughts,
            'has_access_to_add_parked_thoughts': has_access_to_add_parked_thoughts,
            'has_access_to_add_expression': has_access_to_add_expression,
            'has_access_to_add_theme': has_access_to_add_theme,
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
            faci = serializer.save(step=2, user_creator=request.user)
            faci.members.create(
                invited=request.user,
                inviting=request.user,
                for_what=FACI_CREATOR_FOR_WHAT,
            )
            link_instance_from_request(faci, request)

        data_for_return = {'id': faci.pk}
        if updated_fields:
            data_for_return['updated'] = updated_fields
            data_for_return['open_block'] = 'members'
        else:
            data_for_return['updated'] = []

        return Response(status=status.HTTP_200_OK, data=data_for_return)


class FaciEditMembersView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        serializer = FaciEditMembersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        mode = data['mode']
        invited = data['invited_user']  # TODO: обработать на фронте 400 {'unvited_username': ['пользователь не найден']}
        faci_canvas = FaciCanvas.objects.get(pk=canvas_id)
        member = Member.objects.filter(invited=invited, faci_canvas=faci_canvas).first()
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

            member = Member(invited=invited, for_what=data['for_what'], inviting=request.user, faci_canvas=faci_canvas)
            member.save()
            faci_canvas.step = 3
            faci_canvas.save()

        data_for_return = {'open_block': 'agenda', 'success': True}
        return Response(status=status.HTTP_200_OK, data=data_for_return)

    def delete(self, canvas_id):
        ...


class FaciAddThemeView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = FaciCanvas.objects.get(pk=canvas_id)
        if not faci:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FaciAddThemeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(faci=faci, user=request.user)

        if faci.step == 3:
            faci.step = 4
            faci.save()

        response_data = {
            'id': serializer.instance.id,
            'updated': list(serializer.validated_data.keys()),
            'open_block': 'preparing',
        }
        return Response(status=status.HTTP_200_OK, data=response_data)


class FaciEditPreparingView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = FaciCanvas.objects.get(pk=canvas_id)
        if faci.user_creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = FaciEditPreparingSerializer(faci, data=request.data)
        serializer.is_valid(raise_exception=True)
        data_for_return = {
            'updated': [
                name for name, value in serializer.validated_data.items() if getattr(faci, name) != value
            ],
        }
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class FaciStartView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = FaciCanvas.objects.get(pk=canvas_id)
        faci.step = 6
        if faci.meeting_status == faci.MEETING_STATUS_STARTED:
            faci.meeting_status = faci.MEETING_STATUS_FINISHED
        else:
            faci.meeting_status = faci.MEETING_STATUS_STARTED
        faci.save()

        data_for_return = {}
        data_for_return['success'] = True
        data_for_return['meeting_status'] = faci.meeting_status
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class FaciAddKeyThoughtsView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
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
        faci = FaciCanvas.objects.get(pk=canvas_id)
        if not faci:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FaciAddParkedThoughtsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(faci=faci, user=request.user)
        return Response(status=status.HTTP_200_OK, data={'updated': list(serializer.validated_data.keys())})


class FaciGetParkedThoughtsView(APIView):
    def post(self, request, canvas_id: int):
        faci = FaciCanvas.objects.get(pk=canvas_id)
        if not faci:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
        serializer = FaciAddExpressionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(status=status.HTTP_200_OK, data={'updated': ['expression']})


class FaciEditAgreementsView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = FaciCanvas.objects.get(pk=canvas_id)
        serializer = FaciEditAgreementsSerializer(faci, data=request.data)
        serializer.is_valid(raise_exception=True)
        data_for_return = {
            'updated': [
                name for name, value in serializer.validated_data.items() if getattr(faci, name) != value
            ],
        }
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=data_for_return)


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


class AddFaciView(APIView):
    AIM_TYPES = {
        'solution': FaciCanvas.AIM_TYPE_SOLUTION,
        'idea': FaciCanvas.AIM_TYPE_IDEA,
        'sync': FaciCanvas.AIM_TYPE_SYNC,
    }

    def post(self, request):
        serializer = AddFaciViewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        faci = FaciCanvas(
            aim=data['aim'],
            if_not_reached=data['if_not_reached'],
            aim_type=self.AIM_TYPES[data['aim_type']],
            solutions=data['solutions'],
        )
        faci.save()
        data_for_return = {'id': faci.id}
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class GetListFaciView(APIView):
    def get(self, request):
        serializer = GetListFaciSerializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        facis = (
            FaciCanvas.objects.all().order_by('-id')
            .values('id', 'aim', 'if_not_reached', 'aim_type')
        )
        facis = facis[(data['page_number']-1)*data['count_on_page']:data['count_on_page']]

        data_for_return = {
            'facis': facis,
            'total': FaciCanvas.objects.count(),
        }
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class SearchUserView(LoginRequiredMixin, APIView):
    def post(self, request):
        search_string = request.POST['search_string']
        usernames = get_user_model().objects.filter(username__contains=search_string).values('username', 'last_name', 'first_name')[:10]
        return Response(status=status.HTTP_200_OK, data=usernames)
