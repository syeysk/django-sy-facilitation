from subprocess import check_output

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from pages.serializers import ProfileViewSerializer


class ServiceServerView(LoginRequiredMixin, APIView):
    def get(self, request):
        context = {}
        return render(request, 'pages/service_server.html', context)

    def post(self, request):
        command = request.POST.get('command')
        message = 'unknown command'
        if command == 'deploy_server':
            message = check_output('cd .. ; git pull origin main', shell=True)
        elif command == 'restart_server':
            message = check_output('touch tmp/restart.txt', shell=True)

        data = {'message': message}
        return Response(status=status.HTTP_200_OK, data=data)


class IntroView(APIView):
    def get(self, request):
        context = {}
        return render(request, 'pages/intro.html', context)


class ProfileView(LoginRequiredMixin, APIView):
    def get(self, request):
        context = {}
        return render(request, 'pages/profile.html', context)

    def post(self, request):
        serializer = ProfileViewSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = request.user
        update_fields = []
        if user.first_name != data['first_name']:
            user.first_name = data['first_name']
            update_fields.append('first_name')

        if user.last_name != data['last_name']:
            user.last_name = data['last_name']
            update_fields.append('last_name')

        if update_fields:
            user.save()

        result_data = {'success': True, 'updated': update_fields}
        return Response(status=status.HTTP_200_OK, data=result_data)
