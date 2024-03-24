from django.urls import path, re_path

from faci.views import (
    FaciEditorView,
    FaciEditAimView,
    FaciEditMembersView,
    FaciEditAgendaView,
    FaciEditPreparingView,
    FaciAddKeyThoughtsView,
    FaciAddParkedThoughtsView,
    FaciEditAgreementsView,
    FaciStartView,
    FaciListView,
    SearchUserView,
    FaciGetParkedThoughtsView,
    FaciAddThemeView,
    FaciGetKeyThoughtsView,
    FaciGetExpressionsView,
    FaciAddExpressionView,
)


urlpatterns = [
    re_path(r'new/aim/$', FaciEditAimView.as_view(), name='faci_editor_create'),
    re_path(r'(?P<canvas_id>[0-9]+)/aim/$', FaciEditAimView.as_view(), name='faci_editor_aim'),
    re_path(r'(?P<canvas_id>[0-9]+)/member/$', FaciEditMembersView.as_view(), name='faci_editor_member'),
    re_path(r'(?P<canvas_id>[0-9]+)/agenda/$', FaciEditAgendaView.as_view(), name='faci_editor_agenda'),
    re_path(r'(?P<canvas_id>[0-9]+)/preparing/$', FaciEditPreparingView.as_view(), name='faci_editor_preparing'),
    re_path(r'(?P<canvas_id>[0-9]+)/start_meeting/$', FaciStartView.as_view(), name='faci_start_meeting'),
    re_path(r'(?P<canvas_id>[0-9]+)/key_thoughts/add/$', FaciAddKeyThoughtsView.as_view(), name='faci_editor_add_key_thoughts'),
    re_path(r'(?P<canvas_id>[0-9]+)/key_thoughts/get/', FaciGetKeyThoughtsView.as_view(), name='faci_editor_get_key_thoughts'),
    re_path(r'(?P<canvas_id>[0-9]+)/parked_thought/get/$', FaciGetParkedThoughtsView.as_view(), name='faci_editor_get_parked_thought'),
    re_path(r'(?P<canvas_id>[0-9]+)/parked_thought/$', FaciAddParkedThoughtsView.as_view(), name='faci_editor_parked_thought'),
    re_path(r'(?P<canvas_id>[0-9]+)/agreements/$', FaciEditAgreementsView.as_view(), name='faci_editor_agreements'),
    re_path(r'(?P<canvas_id>[0-9]+)/add_theme/$', FaciAddThemeView.as_view(), name='faci_editor_add_theme'),
    re_path(r'(?P<canvas_id>[0-9]+)/expressions/get/', FaciGetExpressionsView.as_view(), name='faci_editor_get_expressions'),
    re_path(r'(?P<canvas_id>[0-9]+)/expressions/add/', FaciAddExpressionView.as_view(), name='faci_editor_add_expression'),

    re_path(r'(?P<canvas_id>[0-9]+)/$', FaciEditorView.as_view(), name='faci_editor'),
    re_path('new/', FaciEditorView.as_view(), name='faci_new'),

    re_path('search_user/', SearchUserView.as_view(), name='search_user'),
    path('', FaciListView.as_view(), name='faci_list'),
]
