from django import forms
from taggit.forms import TagField

from extras.forms import AddRemoveTagsForm, CustomFieldForm, CustomFieldBulkEditForm, CustomFieldFilterForm
from utilities.forms import (
    APISelect, APISelectMultiple, BootstrapMixin, ChainedFieldsMixin, ChainedModelChoiceField, CommentField,
    FilterChoiceField, SlugField,
)
from tenancy.forms import TenancyForm
from .models import Contact, ContactGroup


#
# Contact groups
#

class ContactGroupForm(BootstrapMixin, forms.ModelForm):
    slug = SlugField()

    class Meta:
        model = ContactGroup
        fields = [
            'name', 'slug',
        ]


class ContactGroupCSVForm(forms.ModelForm):
    slug = SlugField()

    class Meta:
        model = ContactGroup
        fields = ContactGroup.csv_headers
        help_texts = {
            'name': 'Group name',
        }


#
# Contacts
#


class ContactForm(BootstrapMixin, TenancyForm, CustomFieldForm):
    slug = SlugField()
    comments = CommentField()
    tags = TagField(
        required=False
    )
    personal_phone = forms.CharField(
        widget= forms.TextInput(
            attrs={
                'maxlength': '12',
                'placeholder': '+12134567689'
            }
        )
    )
    office_phone = forms.CharField(
        widget= forms.TextInput(
            attrs={
                'maxlength': '12',
                'placeholder': '+12134567689'
            }
        )
    )

    class Meta:
        model = Contact
        fields = [
            'name',
            'slug',
            'group',
            'tenant_group',
            'tenant',
            'personal_phone', 
            'office_phone',
            'email',
            'available',
            'unavailable',
            'description',
            'tags',
        ]
        widgets = {
            'group': APISelect(
                api_url="/api/contacts/contact-groups/"
            ),
            'tenant': APISelect(
                api_url="/api/tenancy/tenants/"
            ),
        },


class ContactCSVForm(forms.ModelForm):
    slug = SlugField()
    group = forms.ModelChoiceField(
        queryset=ContactGroup.objects.all(),
        required=False,
        to_field_name='name',
        help_text='Name of parent group',
        error_messages={
            'invalid_choice': 'Group not found.'
        }
    )

    class Meta:
        model = Contact
        fields = Contact.csv_headers
        help_texts = {
            'name': 'Contact name',
            'comments': 'Free-form comments'
        }


class ContactBulkEditForm(BootstrapMixin, AddRemoveTagsForm, CustomFieldBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Contact.objects.all(),
        widget=forms.MultipleHiddenInput()
    )
    group = forms.ModelChoiceField(
        queryset=ContactGroup.objects.all(),
        required=False,
        widget=APISelect(
            api_url="/api/contacts/contact-groups/"
        )
    )

    class Meta:
        nullable_fields = [
            'group',
        ]


class ContactFilterForm(BootstrapMixin, CustomFieldFilterForm):
    model = Contact
    q = forms.CharField(
        required=False,
        label='Search'
    )
    group = FilterChoiceField(
        queryset=ContactGroup.objects.all(),
        to_field_name='slug',
        null_label='-- None --',
        widget=APISelectMultiple(
            api_url="/api/contacts/contact-groups/",
            value_field="slug",
            null_option=True,
        )
    )


#
# Form extensions
#

class ContactsForm(ChainedFieldsMixin, forms.Form):
    contact_group = forms.ModelChoiceField(
        queryset=ContactGroup.objects.all(),
        required=False,
        widget=APISelect(
            api_url="/api/contacts/contact-groups/",
            filter_for={
                'contact': 'group_id',
            },
            attrs={
                'nullable': 'true',
            }
        )
    )
    contact = ChainedModelChoiceField(
        queryset=Contact.objects.all(),
        chains=(
            ('group', 'contact_group'),
        ),
        required=False,
        widget=APISelect(
            api_url='/api/contacts/contacts/'
        )
    )

    def __init__(self, *args, **kwargs):

        # Initialize helper selector
        instance = kwargs.get('instance')
        if instance and instance.contact is not None:
            initial = kwargs.get('initial', {}).copy()
            initial['contact_group'] = instance.contact.group
            kwargs['initial'] = initial
            print('hola')

        super().__init__(*args, **kwargs)


class ContactsFilterForm(forms.Form):
    contact_group = FilterChoiceField(
        queryset=ContactGroup.objects.all(),
        to_field_name='slug',
        null_label='-- None --',
        widget=APISelectMultiple(
            api_url="/api/contacts/contact-groups/",
            value_field="slug",
            null_option=True,
            filter_for={
                'contact': 'group'
            }
        )
    )
    contact = FilterChoiceField(
        queryset=Contact.objects.all(),
        to_field_name='slug',
        null_label='-- None --',
        widget=APISelectMultiple(
            api_url="/api/contacts/contacts/",
            value_field="slug",
            null_option=True,
        )
    )
