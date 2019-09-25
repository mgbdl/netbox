from rest_framework import serializers

from contacts.models import Contact, ContactGroup
from utilities.api import WritableNestedSerializer

__all__ = [
    'NestedContactGroupSerializer',
    'NestedContactSerializer',
]


#
# Contacts
#

class NestedContactGroupSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='contacts-api:contactgroup-detail')
    contact_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ContactGroup
        fields = ['id', 'url', 'name', 'slug', 'contact_count']


class NestedContactSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='contacts-api:contact-detail')

    class Meta:
        model = Contact
        fields = ['id', 'url', 'name', 'slug']
