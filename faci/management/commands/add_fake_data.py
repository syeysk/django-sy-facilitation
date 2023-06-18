from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from faci.models import FaciCanvas, Member

USERS_DATA = (
    ('clever_cat', 'Иосиф', 'Рыбечевский'),
    ('strong_puma', 'Robert', 'Keeyosaki'),
    ('PerfectBird', 'Аркадий', 'Птицин'),
    ('OlegFantom', 'Олег', 'Фантомный'),
    ('big123burger', 'Felis', 'Silvestris'),
)

CANVASES_DATA = (
    {
        'step_zero': {
            'user_creator': 'clever_cat',
            'step': 2,
        },
        'step_one': {
            'aim': 'Стоит ли использовать технологию VR на сайте',
            'if_not_reached': 'Недостаточный охват аудитории',
            'aim_type': FaciCanvas.AIM_TYPE_SOLUTION,
            'solutions': '',
        },
        'step_two': (),
    },
    {
        'step_zero': {
            'user_creator': 'strong_puma',
            'step': 4,
        },
        'step_one': {
            'aim': 'Придумать бизнес-идею для нового направления',
            'if_not_reached': 'сохранится недостаточная диверсификация бизнеса',
            'aim_type': FaciCanvas.AIM_TYPE_IDEA,
            'solutions': '',
        },
        'step_two': (
            ('PerfectBird', 'специалист по мозговому штурму'),
            ('big123burger', 'рыночный аналитик'),
        ),
        'step_three': (),
    },
)


def add_user(username, first_name, last_name):
    user_data = {
        'username': username,
        'password': f'1234-{username}',
        'email': '',
        'first_name': first_name,
        'last_name': last_name,
        'is_active': False,
    }
    user = User(**user_data)
    user.set_password(user_data['password'])
    user.save()


def add_canvas(step_zero, step_one, step_two):
    user_creator = User.objects.get(username=step_zero['user_creator'])
    canvas = FaciCanvas(user_creator=user_creator, step=step_zero['step'], **step_one)
    canvas.save()
    Member(invited=user_creator, inviting=user_creator, for_what='Инициатор встречи', faci_canvas=canvas).save()
    for invited, for_what in step_two:
        user_invited = User.objects.get(username=invited)
        Member(invited=user_invited, inviting=user_creator, for_what=for_what, faci_canvas=canvas).save()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--delete', action='store_true')

    @staticmethod
    def add_data():
        for user_data in USERS_DATA:
            add_user(*user_data)

        print('Demo users was added')

        for canvas_data in CANVASES_DATA:
            add_canvas(canvas_data['step_zero'], canvas_data['step_one'], canvas_data['step_two'])

        print('Demo canvases was added')

    @staticmethod
    def delete_data():
        usernames = [username for username, _, __ in USERS_DATA]
        FaciCanvas.objects.filter(user_creator__username__in=usernames).delete()
        print('Demo users was deleted')
        User.objects.filter(username__in=usernames).delete()
        print('Demo canvases was deleted')
        Member.objects.filter(inviting__username__in=usernames).delete()
        print('Demo members was deleted')

    def handle(self, *args, **options):
        if options['delete']:
            self.delete_data()
        else:
            self.add_data()
