import django_filters
from .models import Contact, ContactGroup


class ContactsFilterSet(django_filters.FilterSet):
    contact_group_id = django_filters.ModelMultipleChoiceFilter(
        field_name='contact__group__id',
        queryset=ContactGroup.objects.all(),
        to_field_name='id',
        label='Contact Group (ID)',
    )
    contact_group = django_filters.ModelMultipleChoiceFilter(
        field_name='contact__group__slug',
        queryset=ContactGroup.objects.all(),
        to_field_name='slug',
        label='Contact Group (slug)',
    )
    contact_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Contact.objects.all(),
        label='Contact (ID)',
    )
    contact = django_filters.ModelMultipleChoiceFilter(
        field_name='contact__slug',
        queryset=Contact.objects.all(),
        to_field_name='slug',
        label='Contact (slug)',
    )
