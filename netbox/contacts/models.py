from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

from extras.models import CustomFieldModel, TaggedItem
from utilities.models import ChangeLoggedModel


class ContactGroup(ChangeLoggedModel):
    """
    An arbitrary collection of Contacts.
    """
    name = models.CharField(
        max_length=50,
        unique=True
    )
    slug = models.SlugField(
        unique=True
    )

    csv_headers = ['name', 'slug']

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "{}?group={}".format(reverse('contacts:contact_list'), self.slug)

    def to_csv(self):
        return (
            self.name,
            self.slug,
        )


class Contact(ChangeLoggedModel, CustomFieldModel):
    """
    A Contact represents an organization served by the NetBox owner. This is typically a customer or an internal
    department.
    """
    name = models.CharField(
        max_length=30,
    )
    slug = models.SlugField(
        unique=True
    )
    group = models.ForeignKey(
        to='contacts.ContactGroup',
        on_delete=models.SET_NULL,
        related_name='contacts',
        blank=True,
        null=True
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='contacts',
        blank=True,
        null=True
    )
    personal_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Personal Phone'
    )
    office_phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Office Phone'
    )
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='E-mail'
    )
    available = models.TimeField(
        blank=True,
        null=True,
    )
    unavailable = models.TimeField(
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=100,
        blank=True,
        help_text='Long-form name (optional)'
    )
    comments = models.TextField(
        blank=True
    )
    custom_field_values = GenericRelation(
        to='extras.CustomFieldValue',
        content_type_field='obj_type',
        object_id_field='obj_id'
    )

    tags = TaggableManager(through=TaggedItem)

    csv_headers = [
        'name',
        'slug',
        'group',
        'tenant',
        'personal_phone', 
        'office_phone',
        'email',
        'available',
        'unavailable',
        'description',]

    class Meta:
        ordering = ['group', 'tenant', 'name',]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('contacts:contact', args=[self.slug])

    def to_csv(self):
        return (
            self.name,
            self.slug,
            self.group.name if self.group else None,
            self.tenant.name if self.tenant else None,
            self.personal_phone, 
            self.office_phone,
            self.email,
            self.available,
            self.unavailable,
            self.description,
            self.comments,
        )
