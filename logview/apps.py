from django.apps import AppConfig


class LogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logview'
    verbose_name = '2. Журнал'
    tooltip="Журнали змін в інформації про сервери та звіти про автоматичні таски, що працюють на серверах"
