import django_filters
from .models import Case

class CaseFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Case.STATUS_CHOICES, label="Status")
    case_type = django_filters.ChoiceFilter(choices=Case.CASE_TYPE_CHOICES, label="Project typr")
    court = django_filters.ChoiceFilter(choices=Case.COURT_CHOICES, label="Zone")

    class Meta:
        model = Case
        fields = ['status', 'case_type', 'court']
