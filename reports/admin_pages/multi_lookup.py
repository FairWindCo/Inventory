from baton.admin import MultipleChoiceListFilter

from info.models import Server


class StatusListFilter(MultipleChoiceListFilter):
    title = 'Статус'
    parameter_name = 'status__in'

    def lookups(self, request, model_admin):
        return Server.ServerState.choices
