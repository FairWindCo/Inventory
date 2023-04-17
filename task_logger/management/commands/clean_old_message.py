from datetime import timedelta

from django.core.management import BaseCommand
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware

from task_logger.models import ServerTaskReport


class Command(BaseCommand):
    help = 'Delete task message older then'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument("days", type=int, action="store", default=30)

    def handle(self, *args, **options):
        days = options["days"]
        delete_before = datetime.now() - timedelta(days=days)
        print("Delete all messages on date: ", delete_before)
        deleted, cont = ServerTaskReport.objects.filter(report_date__lte=make_aware(delete_before)).delete()
        print(f"DELETED: {deleted}")