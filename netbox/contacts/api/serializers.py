from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from extras.api.customfields import CustomFieldModelSerializer
from contacts.models import Contact, ContactGroup
from utilities.api import ValidatedModelSerializer
from .nested_serializers import *


#
# Contacts
#

class ContactGroupSerializer(ValidatedModelSerializer):
    contact_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ContactGroup
        fields = ['id', 'name', 'slug', 'contact_count']


class ContactSerializer(TaggitSerializer, CustomFieldModelSerializer):
    group = NestedContactGroupSerializer(required=False)
    tags = TagListSerializerField(required=False)
    circuit_count = serializers.IntegerField(read_only=True)
    device_count = serializers.IntegerField(read_only=True)
    ipaddress_count = serializers.IntegerField(read_only=True)
    prefix_count = serializers.IntegerField(read_only=True)
    rack_count = serializers.IntegerField(read_only=True)
    site_count = serializers.IntegerField(read_only=True)
    virtualmachine_count = serializers.IntegerField(read_only=True)
    vlan_count = serializers.IntegerField(read_only=True)
    vrf_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'slug', 'group', 'tenant', 'personal_phone', 'office_phone', 'description', 'comments', 'tags', 'custom_fields', 'created',
            'last_updated', 'circuit_count', 'device_count', 'ipaddress_count', 'prefix_count', 'rack_count',
            'site_count', 'virtualmachine_count', 'vlan_count', 'vrf_count',
        ]
