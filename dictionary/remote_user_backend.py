from django.conf import settings
from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.contrib.auth.models import Group


class CustomRemoteUserMiddleware(RemoteUserMiddleware):
    header = 'HTTP_X_FORWARDED_SSO'

    def process_request(self, request):
        if hasattr(settings, 'DEBUG_HEADER_REQUEST') and settings.DEBUG_HEADER_REQUEST:
            print('META\n', "\n".join(request.META.keys()))
            print('HEAD\n', "\n".join(request.headers.keys()))
            print('ENV\n', "\n".join(request.environ.keys()))
            print(f'{self.header}:{request.META.get(self.header)}')
        super().process_request(request)

    def clean_username(self, username, request):
        return super().clean_username(username, request)


class CustomUserBackend(RemoteUserBackend):

    def authenticate(self, request, remote_user):
        print(f'Auth username {remote_user}')
        return super().authenticate(request, remote_user)

    def clean_username(self, username):
        print(f'Clean username {username}')
        return super().clean_username(username)

    def configure_user(self, request, user):
        user = super().configure_user(request, user)
        try:
            user.is_staff = True
            user.is_active = True
            try:
                group = Group.objects.get(name='viewer')
                user.groups.add(group)
            except Group.DoesNotExist:
                pass

            user.save()
        except Exception:
            pass
        print(f'Configure username {user}')
        return user
