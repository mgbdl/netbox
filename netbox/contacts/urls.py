from django.urls import path

from extras.views import ObjectChangeLogView
from . import views
from .models import Contact, ContactGroup

app_name = 'contacts'
urlpatterns = [

    # Contact groups
    path(r'contact-groups/', views.ContactGroupListView.as_view(), name='contactgroup_list'),
    path(r'contact-groups/add/', views.ContactGroupCreateView.as_view(), name='contactgroup_add'),
    path(r'contact-groups/import/', views.ContactGroupBulkImportView.as_view(), name='contactgroup_import'),
    path(r'contact-groups/delete/', views.ContactGroupBulkDeleteView.as_view(), name='contactgroup_bulk_delete'),
    path(r'contact-groups/<slug:slug>/edit/', views.ContactGroupEditView.as_view(), name='contactgroup_edit'),
    path(r'contact-groups/<slug:slug>/changelog/', ObjectChangeLogView.as_view(), name='contactgroup_changelog', kwargs={'model': ContactGroup}),

    # Contacts
    path(r'contacts/', views.ContactListView.as_view(), name='contact_list'),
    path(r'contacts/add/', views.ContactCreateView.as_view(), name='contact_add'),
    path(r'contacts/import/', views.ContactBulkImportView.as_view(), name='contact_import'),
    path(r'contacts/edit/', views.ContactBulkEditView.as_view(), name='contact_bulk_edit'),
    path(r'contacts/delete/', views.ContactBulkDeleteView.as_view(), name='contact_bulk_delete'),
    path(r'contacts/<slug:slug>/', views.ContactView.as_view(), name='contact'),
    path(r'contacts/<slug:slug>/edit/', views.ContactEditView.as_view(), name='contact_edit'),
    path(r'contacts/<slug:slug>/delete/', views.ContactDeleteView.as_view(), name='contact_delete'),
    path(r'contacts/<slug:slug>/changelog/', ObjectChangeLogView.as_view(), name='contact_changelog', kwargs={'model': Contact}),

]
