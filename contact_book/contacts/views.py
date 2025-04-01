# contacts/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Contact, ContactGroup
from .forms import ContactForm
from ajax_datatable.views import AjaxDatatableView
from django.shortcuts import render


class ContactListView(ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'


class ContactAjaxDatatableView(AjaxDatatableView):
    model = Contact
    title = 'Contacts'
    initial_order = [["name", "asc"]]
    length_menu = [[10, 20, 50, 100], [10, 20, 50, 100]]
    search_values_separator = '+'

    column_defs = [
        {'name': 'name', 'visible': True, 'title': 'Name'},
        {'name': 'phone_number', 'visible': True, 'title': 'Phone Number'},
        {'name': 'email', 'visible': True, 'title': 'Email'},
        {'name': 'contact_group__name', 'visible': True,
            'title': 'Group', 'foreign_field': 'contact_group__name'},
        {'name': 'actions', 'title': 'Actions',
            'searchable': False, 'orderable': False},
    ]

    def customize_row(self, row, obj):
        row['actions'] = render_to_string(
            'contacts/includes/contact_actions.html',
            {'contact': obj}
        )
        return row


class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/includes/contact_form.html'
    success_url = reverse_lazy('contact_list')

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                form = self.get_form()
                return render(request, self.template_name, {'form': form})
            return super().get(request, *args, **kwargs)
        except (Exception) as e:
            print(f"Exception occured:{e}")

    def form_valid(self, form):
        contact = form.save()
        data = {
            'success': True,
            'message': 'Contact created successfully!',
            'contact': {
                'id': contact.id,
                'name': contact.name,
                'phone_number': contact.phone_number,
                'email': contact.email or '',
                'contact_group': contact.contact_group.name,
            }
        }
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {
            'success': False,
            'html_form': render_to_string(
                'contacts/contact_form.html',
                {'form': form},
                request=self.request
            )
        }
        return JsonResponse(data)


class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/includes/contact_form.html'
    success_url = reverse_lazy('contact_list')

    def form_valid(self, form):
        contact = form.save()
        data = {
            'success': True,
            'message': 'Contact updated successfully!',
            'contact': {
                'id': contact.id,
                'name': contact.name,
                'phone_number': contact.phone_number,
                'email': contact.email or '',
                'contact_group': contact.contact_group.name,
            }
        }
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {
            'success': False,
            'html_form': render_to_string(
                'contacts/includes/contact_form.html',
                {'form': form},
                request=self.request
            )
        }
        return JsonResponse(data)


class ContactDeleteView(DeleteView):
    model = Contact
    

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({
            'success': True,
            'message': 'Contact deleted successfully!'
        })
    
    success_url = reverse_lazy('contact_list')
