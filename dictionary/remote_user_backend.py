from django.contrib.auth.backends import RemoteUserBackend


class CustomUserBackend(RemoteUserBackend):
    def authenticate(self, request, remote_user):
        print(f'Auth username {remote_user}')
        return super().authenticate(request, remote_user)

    def clean_username(self, username):
        print(f'Clean username {username}')
        return super().clean_username(username)

    def configure_user(self, request, user):
        print(f'Configure username {user}')
        return super().configure_user(request, user)