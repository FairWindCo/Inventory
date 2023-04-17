from django.core.management import BaseCommand

from info.models.applications import HostScheduledTask


class Command(BaseCommand):
    help = 'Delete info about deleted tasks'

    def handle(self, *args, **options):
        print('need delete tasks:', HostScheduledTask.objects.filter(is_removed=True).count())
        HostScheduledTask.objects.filter(is_removed=True).delete()
        print('after delete tasks:', HostScheduledTask.objects.filter(is_removed=True).count())
