# contacts/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Contact, ContactGroup
from .forms import ContactForm
from ajax_datatable.views import AjaxDatatableView
from django.shortcuts import render, get_object_or_404


class ContactListView(ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'


class ContactAjaxDatatableView(AjaxDatatableView):
    model = Contact
    title = 'Contacts'
    search_fields: list[str] = ["name", "phone_number", "email","contact_group__name"]
    column_defs: list[object] = [
        {"name": "id", "title": "id", "visible": True, "orderable": True},
        {"name": "name", "title": "Title", "orderable": True},
        {"name": "phone_number", "title": "Content", "orderable": False},
        {"name": "email", "title": "Category", "orderable": True},
        {'name': 'contact_group__name', 'visible': True, 'title': 'Group', 'foreign_field': 'contact_group__name'},
    ]


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
        try:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                self.object = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Contact created successfully!',
                    'id': self.object.pk,
                })
            return super().form_valid(form)
        except (Exception) as e:
            print(f"Exception occured:{e}")

    def form_invalid(self, form):
        try:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'html': render_to_string(self.template_name, {'form': form}, request=self.request)
                })
            return super().form_invalid(form)
        except (Exception) as e:
            print(f"Exception occured:{e}")


class ContactUpdateView(UpdateView):
    try:
        model = Contact
        form_class = ContactForm
        template_name: str = 'contacts/includes/contact_form.html'
        success_url = reverse_lazy('contact_list')

    except (Exception) as e:
        print(f"Exception occured:{e}")

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                self.object = self.get_object()
                form = self.get_form()
                context = {
                    'form': form,
                    'object': self.object,
                }

                return render(request, self.template_name, context)
            return super().get(request, *args, **kwargs)
        except (Exception) as e:
            print(f"Exception occured:{e}")

    def form_valid(self, form):
        # Handle AJAX form submission
        try:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Check if image field is empty in the POST but the object already has an image
                if not self.request.FILES.get('image') and 'image-clear' not in self.request.POST:
                    # Keep the existing image
                    self.object = form.save(commit=False)
                    # Get the existing Blog object and its image
                    existing_blog = get_object_or_404(Contact, pk=self.object.pk)
                    self.object.image = existing_blog.image

                    self.object.save()
                    form.save_m2m()  # Save many-to-many relationships if any
                else:
                    self.object = form.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Blog updated successfully!',
                    'id': self.object.pk,
                })
            return super().form_valid(form)
        except (Exception) as e:
            print(f"Exception occured:{e}")

    def form_invalid(self, form):
        # Handle AJAX form submission with errors
        try:
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                self.object = self.get_object()  # Need to get the object for the template
                context = {
                    'form': form,
                    'object': self.object,
                    'has_image': bool(self.object.image)
                }
                if self.object.image:
                    context['image_url'] = self.object.image.url

                return JsonResponse(
                    {
                        "success": False,
                        'html': render_to_string(self.template_name, context, request=self.request)
                    }
                )
            return super().form_invalid(form)
        except (Exception) as e:
            print(f"Exception occured:{e}")


class ContactDeleteView(DeleteView):
    model = Contact
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({
            'success': True,
            'message': 'Contact deleted successfully!'
        })
    
    success_url = reverse_lazy('contact_list')
