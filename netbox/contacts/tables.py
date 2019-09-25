import django_tables2 as tables

from utilities.tables import BaseTable, ToggleColumn
from .models import Contact, ContactGroup

CONTACTGROUP_ACTIONS = """
<a href="{% url 'contacts:contactgroup_changelog' slug=record.slug %}" class="btn btn-default btn-xs" title="Changelog">
    <i class="fa fa-history"></i>
</a>
{% if perms.contacts.change_contactgroup %}
    <a href="{% url 'contacts:contactgroup_edit' slug=record.slug %}?return_url={{ request.path }}" class="btn btn-xs btn-warning"><i class="glyphicon glyphicon-pencil" aria-hidden="true"></i></a>
{% endif %}
"""

COL_CONTACT = """
{% if record.contact %}
    <a href="{% url 'contacts:contact' slug=record.contact.slug %}" title="{{ record.contact.description }}">{{ record.contact }}</a>
{% else %}
    &mdash;
{% endif %}
"""


#
# Contact groups
#

class ContactGroupTable(BaseTable):
    pk = ToggleColumn()
    name = tables.LinkColumn(verbose_name='Name')
    contact_count = tables.Column(verbose_name='Contacts')
    slug = tables.Column(verbose_name='Slug')
    actions = tables.TemplateColumn(
        template_code=CONTACTGROUP_ACTIONS, attrs={'td': {'class': 'text-right noprint'}}, verbose_name=''
    )

    class Meta(BaseTable.Meta):
        model = ContactGroup
        fields = ('pk', 'name', 'contact_count', 'slug', 'actions')


#
# Contacts
#

class ContactTable(BaseTable):
    pk = ToggleColumn()
    first_name = tables.LinkColumn()
    tenant = tables.LinkColumn()
    group = tables.LinkColumn()

    class Meta(BaseTable.Meta):
        model = Contact
        fields = ('pk', 'name', 'tenant', 'group', 'description')
