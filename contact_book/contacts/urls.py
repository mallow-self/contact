from django.urls import path
from .views import (
    ContactListView, ContactCreateView, ContactUpdateView,
    ContactDeleteView, ContactAjaxDatatableView
)

urlpatterns = [
    path('', ContactListView.as_view(), name='contact_list'),
    path('api/contacts/', ContactAjaxDatatableView.as_view(), name='contact_data'),
    path('create/', ContactCreateView.as_view(), name='contact_create'),
    path('update/<int:pk>/', ContactUpdateView.as_view(), name='contact_update'),
    path('delete/<int:pk>/', ContactDeleteView.as_view(), name='contact_delete'),
]
