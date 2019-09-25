from circuits.models import Circuit
from dcim.models import Device, Rack, Site
from extras.api.views import CustomFieldModelViewSet
from ipam.models import IPAddress, Prefix, VLAN, VRF
from contacts import filters
from contacts.models import Contact, ContactGroup
from utilities.api import FieldChoicesViewSet, ModelViewSet
from utilities.utils import get_subquery
from virtualization.models import VirtualMachine
from . import serializers


#
# Field choices
#

class ContactsFieldChoicesViewSet(FieldChoicesViewSet):
    fields = ()


#
# Contact Groups
#

class ContactGroupViewSet(ModelViewSet):
    queryset = ContactGroup.objects.annotate(
        contact_count=get_subquery(Contact, 'group')
    )
    serializer_class = serializers.ContactGroupSerializer
    filterset_class = filters.ContactGroupFilter


#
# Contacts
#

class ContactViewSet(CustomFieldModelViewSet):
    queryset = Contact.objects.prefetch_related(
        'group', 'tags'
    ).annotate(
        # circuit_count=get_subquery(Circuit, 'tenant'),
        # device_count=get_subquery(Device, 'tenant'),
        # ipaddress_count=get_subquery(IPAddress, 'tenant'),
        # prefix_count=get_subquery(Prefix, 'tenant'),
        # rack_count=get_subquery(Rack, 'tenant'),
        site_count=get_subquery(Site, 'contact'),
        # virtualmachine_count=get_subquery(VirtualMachine, 'tenant'),
        # vlan_count=get_subquery(VLAN, 'tenant'),
        # vrf_count=get_subquery(VRF, 'tenant')
    )
    serializer_class = serializers.ContactSerializer
    filterset_class = filters.ContactFilter
