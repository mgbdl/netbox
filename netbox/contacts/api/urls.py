from rest_framework import routers

from . import views


class ContactsRootView(routers.APIRootView):
    """
    Contacts API root view
    """
    def get_view_name(self):
        return 'Contacts'


router = routers.DefaultRouter()
router.APIRootView = ContactsRootView

# Field choices
router.register(r'_choices', views.ContactsFieldChoicesViewSet, basename='field-choice')

# Contacts
router.register(r'contact-groups', views.ContactGroupViewSet)
router.register(r'contacts', views.ContactViewSet)

app_name = 'contacts-api'
urlpatterns = router.urls
