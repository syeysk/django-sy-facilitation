from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django_sy_framework.linker.utils import link_instance_from_request
from faci.models import FaciCanvas, Member
from faci.serializers import (
    AddFaciViewSerializer,
    GetListFaciSerializer,
    FaciEditAimSerializer,
    FaciEditMembersSerializer,
    FaciEditAgendaSerializer,
    FaciEditPreparingSerializer,
    FaciEditKeyThoughtsSerializer,
    FaciAddParkedThoughtsSerializer,
    FaciEditAgreementsSerializer,
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
            agendas = [
                {
                    'invited': member.invited.username,
                    'themes': member.themes,
                    'themes_duration': member.themes_duration,
                    'questions': member.questions,
                    'fundamental_objections': member.fundamental_objections,
                    'suggested_solutions': member.suggested_solutions,
                    'counter_offer': member.counter_offer,
                    'self': member.invited.username == request.user.username,
                }
                for member in faci.members.all()
            ]
            has_access_to_edit_preparing = request.user == faci.user_creator
            has_access_to_add_members = request.user.is_authenticated
        else:
            if not request.user.is_authenticated:
                return redirect('custom_login_page')

            faci = FaciCanvas()
            step = 1
            username = request.user.username
            members = [{'invited': username, 'for_what': FACI_CREATOR_FOR_WHAT, 'inviting': username}]
            agendas = [
                {
                    'invited': username,
                    'themes': '',
                    'themes_duration': 0,
                    'questions': '',
                    'fundamental_objections': '',
                    'suggested_solutions': '',
                    'counter_offer': '',
                    'self': True,
                },
            ]
            has_access_to_edit_preparing = True
            has_access_to_add_members = True

        context = {
            'faci': faci,
            'faci_json': {
                'dt_meeting': faci.dt_meeting.strftime('%Y-%m-%dT%H:%M') if faci.dt_meeting else None,
                'duration': faci.duration,
                'place': faci.place.strip(),
                'meeting_status': faci.meeting_status,
                'key_thoughts': faci.key_thoughts,
            },
            'aim_type_choices': FaciCanvas.AIM_TYPE_CHOICES,
            'step': step,
            'members': members,
            'agendas': agendas,
            'has_access_to_edit_preparing': has_access_to_edit_preparing,
            'has_access_to_add_members': has_access_to_add_members,
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
            updated_fields = serializer.fields.keys()
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

        data_for_return = {}
        data_for_return['open_block'] = 'agenda'
        data_for_return['success'] = True
        return Response(status=status.HTTP_200_OK, data=data_for_return)

    def delete(self, canvas_id):
        ...


class FaciEditAgendaView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        serializer = FaciEditAgendaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        faci_canvas = FaciCanvas.objects.get(pk=canvas_id)
        member = Member.objects.get(invited=request.user, faci_canvas=faci_canvas)
        updated_fields = [name for name, value in data.items() if getattr(member, name) != value]
        member.themes = data['themes']
        member.themes_duration = data['themes_duration']
        member.questions = data['questions']
        member.fundamental_objections = data['fundamental_objections']
        member.suggested_solutions = data['suggested_solutions']
        member.counter_offer = data['counter_offer']
        member.save()
        faci_canvas.step = 4
        faci_canvas.save()

        data_for_return = {'open_block': 'preparing', 'updated': updated_fields}
        return Response(status=status.HTTP_200_OK, data=data_for_return)


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


class FaciEditKeyThoughtsView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = FaciCanvas.objects.get(pk=canvas_id)
        if not faci:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if faci.user_creator.pk != request.user.pk:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = FaciEditKeyThoughtsSerializer(faci, data=request.data)
        serializer.is_valid(raise_exception=True)
        data_for_return = {
            'updated': [
                name for name, value in serializer.validated_data.items() if getattr(faci, name) != value
            ],
        }
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=data_for_return)


class FaciAddParkedThoughtsView(LoginRequiredMixin, APIView):
    def post(self, request, canvas_id):
        faci = FaciCanvas.objects.get(pk=canvas_id)
        if not faci:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FaciAddParkedThoughtsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(faci=faci, user=request.user)
        return Response(status=status.HTTP_200_OK, data={'updated': list(serializer.validated_data.keys())})


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
