from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from circuits.models import Circuit
from dcim.models import Site, Rack, Device, RackReservation
from ipam.models import IPAddress, Prefix, VLAN, VRF
from utilities.views import (
    BulkDeleteView, BulkEditView, BulkImportView, ObjectDeleteView, ObjectEditView, ObjectListView,
)
from virtualization.models import VirtualMachine
from . import filters, forms, tables
from .models import Contact, ContactGroup


#
# Contact groups
#

class ContactGroupListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'contacts.view_contactgroup'
    queryset = ContactGroup.objects.annotate(contact_count=Count('contacts'))
    table = tables.ContactGroupTable
    template_name = 'contacts/contactgroup_list.html'


class ContactGroupCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'contacts.add_contactgroup'
    model = ContactGroup
    model_form = forms.ContactGroupForm
    default_return_url = 'contacts:contactgroup_list'


class ContactGroupEditView(ContactGroupCreateView):
    permission_required = 'contacts.change_contactgroup'


class ContactGroupBulkImportView(PermissionRequiredMixin, BulkImportView):
    permission_required = 'contacts.add_contactgroup'
    model_form = forms.ContactGroupCSVForm
    table = tables.ContactGroupTable
    default_return_url = 'contacts:contactgroup_list'


class ContactGroupBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'contacts.delete_contactgroup'
    queryset = ContactGroup.objects.annotate(contact_count=Count('contacts'))
    table = tables.ContactGroupTable
    default_return_url = 'contacts:contactgroup_list'


#
#  Contacts
#

class ContactListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'contacts.view_contact'
    queryset = Contact.objects.prefetch_related('group')
    filter = filters.ContactFilter
    filter_form = forms.ContactFilterForm
    table = tables.ContactTable
    template_name = 'contacts/contact_list.html'


class ContactView(PermissionRequiredMixin, View):
    permission_required = 'contacts.view_contact'

    def get(self, request, slug):

        contact = get_object_or_404(Contact, slug=slug)
        stats = {
            'site_count': Site.objects.filter(contact=contact).count(),
            # 'rack_count': Rack.objects.filter(contact=contact).count(),
            # 'rackreservation_count': RackReservation.objects.filter(contact=contact).count(),
            # 'device_count': Device.objects.filter(contact=contact).count(),
            # 'vrf_count': VRF.objects.filter(contact=contact).count(),
            # 'prefix_count': Prefix.objects.filter(contact=contact).count(),
            # 'ipaddress_count': IPAddress.objects.filter(contact=contact).count(),
            # 'vlan_count': VLAN.objects.filter(contact=contact).count(),
            # 'circuit_count': Circuit.objects.filter(contact=contact).count(),
            # 'virtualmachine_count': VirtualMachine.objects.filter(contact=contact).count(),
        }

        return render(request, 'contacts/contact.html', {
            'contact': contact,
            'stats': stats,
        })


class ContactCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'contacts.add_contact'
    model = Contact
    model_form = forms.ContactForm
    template_name = 'contacts/contact_edit.html'
    default_return_url = 'contacts:contact_list'


class ContactEditView(ContactCreateView):
    permission_required = 'contacts.change_contact'


class ContactDeleteView(PermissionRequiredMixin, ObjectDeleteView):
    permission_required = 'contacts.delete_contact'
    model = Contact
    default_return_url = 'contacts:contact_list'


class ContactBulkImportView(PermissionRequiredMixin, BulkImportView):
    permission_required = 'contacts.add_contact'
    model_form = forms.ContactCSVForm
    table = tables.ContactTable
    default_return_url = 'contacts:contact_list'


class ContactBulkEditView(PermissionRequiredMixin, BulkEditView):
    permission_required = 'contacts.change_contact'
    queryset = Contact.objects.prefetch_related('group')
    filter = filters.ContactFilter
    table = tables.ContactTable
    form = forms.ContactBulkEditForm
    default_return_url = 'contacts:contact_list'


class ContactBulkDeleteView(PermissionRequiredMixin, BulkDeleteView):
    permission_required = 'contacts.delete_contact'
    queryset = Contact.objects.prefetch_related('group')
    filter = filters.ContactFilter
    table = tables.ContactTable
    default_return_url = 'contacts:contact_list'
