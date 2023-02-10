from django.apps import AppConfig


class TaskLoggerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_logger'
    verbose_name = ' Звіти про роботу задач на серверах'
