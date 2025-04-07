# contacts/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Contact, ContactGroup, User
from .forms import ContactForm, RegisterForm, LoginForm
from ajax_datatable.views import AjaxDatatableView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .permissions import OwnershipRequiredMixin, AdminRequiredMixin, role_required


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "USER"  # Default role
            user.save()
            messages.success(request, "Registration successful. You can now login.")
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.email}!")
                return redirect("contact_list")
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        user = self.request.user

        # Super admins can see all contacts
        if user.role == "SUPER_ADMIN":
            return Contact.objects.all()

        # Admins can see all contacts they own
        elif user.role == "ADMIN":
            return Contact.objects.filter(owner=user)

        # Regular users can only see their own contacts
        else:
            return Contact.objects.filter(owner=user)


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
        {'name': 'owner'}
    ]


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/includes/contact_form.html'
    success_url = reverse_lazy('contact_list')

    def get(self, request, *args, **kwargs):
        # If AJAX request, return only the form
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                form = self.get_form()

                user = self.request.user
                if user.role == 'SUPER_ADMIN':
                    form.fields['contact_group'].queryset = ContactGroup.objects.all()
                else:
                    form.fields['contact_group'].queryset = ContactGroup.objects.filter(owner=user)

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
                html_form = render_to_string(self.template_name, {'form': form}, request=self.request)
                return JsonResponse({
                    'success': False,
                    'html_form': html_form
                })
            return super().form_invalid(form)
        except (Exception) as e:
            print(f"Exception occurred:{e}")


class ContactUpdateView(LoginRequiredMixin, OwnershipRequiredMixin, UpdateView):
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

                user = self.request.user
                if user.role == 'SUPER_ADMIN':
                    form.fields['contact_group'].queryset = ContactGroup.objects.all()
                else:
                    form.fields['contact_group'].queryset = ContactGroup.objects.filter(owner=user)

                context = {
                    "form": form,
                    "object": self.object,
                    "has_image": bool(self.object.contact_picture),
                }
                if self.object.contact_picture:
                    context["image_url"] = self.object.contact_picture.url

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
                    self.object.contact_picture = existing_blog.contact_picture

                    self.object.save()
                    form.save_m2m()  # Save many-to-many relationships if any
                else:
                    self.object = form.save()

                return JsonResponse({
                    'success': True,
                    'message': 'Contact updated successfully!',
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
                    "form": form,
                    "object": self.object,
                    "has_image": bool(self.object.contact_picture),
                }
                if self.object.contact_picture:
                    context["image_url"] = self.object.contact_picture.url

                return JsonResponse(
                    {
                        "success": False,
                        'html_form': render_to_string(self.template_name, context, request=self.request)
                    }
                )
            return super().form_invalid(form)
        except (Exception) as e:
            print(f"Exception occured:{e}")


class ContactDeleteView(LoginRequiredMixin, OwnershipRequiredMixin, DeleteView):
    model = Contact
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({
            'success': True,
            'message': 'Contact deleted successfully!'
        })

    success_url = reverse_lazy('contact_list')


@login_required
@role_required(["SUPER_ADMIN", "ADMIN"])
def manage_users(request):
    """View to manage users - available only to admins and super admins"""
    # Super admin can see all users except other super admins
    if request.user.role == "SUPER_ADMIN":
        users = User.objects.exclude(role="SUPER_ADMIN").exclude(id=request.user.id)
    # Admin can only see regular users
    else:
        users = User.objects.filter(role="USER")

    return render(request, "admin/manage_users.html", {"users": users})
