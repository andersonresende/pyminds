from rest_framework import permissions

from django.conf import settings


class SlackTokenPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        token = request.POST.get('token')
        return token and token == settings.SLACK_TOKEN_API
