from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_protect
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import render
from django.core.mail import send_mail
from itertools import groupby
from operator import attrgetter


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', { 'destinations': all_destinations})

def grouped_opinions(request):
    opinions = models.Opinions.objects.all().order_by('cruise')
    grouped_opinions = {k: list(v) for k, v in groupby(opinions, key=attrgetter('cruise'))}
    return render(request, 'opinions_info.html', {'grouped_opinions': grouped_opinions})

class DestinationDetailView(generic.DetailView):
    template_name = 'destination_detail.html'
    model = models.Destination
    context_object_name = 'destination'

class DestinationCreateView(generic.CreateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name','description']

class DestinationUpdateView(generic.UpdateView):
    model = models.Destination
    template_name = 'destination_form.html'
    fields = ['name','description']

class DestinationDeleteView(generic.DeleteView):
    model = models.Destination
    template_name = 'destination_confirm_delete.html'
    success_url = reverse_lazy('destinations')

class CruiseDetailView(generic.DetailView):
    template_name = 'cruise_detail.html'
    model = models.Cruise
    context_object_name = 'cruise'

class InfoRequestCreate(SuccessMessageMixin, generic.CreateView):
    template_name = 'info_request_create.html'
    model = models.InfoRequest
    fields = ['name', 'email', 'cruise', 'notes']
    success_url = reverse_lazy('index')
    success_message = 'Thank you, %(name)s! We will email you when we have more information about %(cruise)s!'

    
def email_notification(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST['name']
        email = request.POST['email']
        cruise = request.POST['cruise']
        # Send email notification
        subject = 'Request Information Received'
        body = f"""
        Dear {name},

        Thank you for your interest in our {cruise} cruise. We have received your request for information and will be in touch soon to answer your questions.

        Regards,
        The Customer Service Team
        """
        from_email = '7903401@alumnos.ufv.es'
        recipient_list = [email]  # Update with the recipient's email address

        send_mail(subject, body, from_email, recipient_list)

        success_message = 'Email sent successfully!'

    return render(request, 'info_request_create.html', {'success_message': success_message})

    
class OpinionsInfo(SuccessMessageMixin, generic.CreateView):
    template_name = 'opinions_info.html'
    model = models.Opinions
    context_object_name = 'opinion'
    
    def form_valid(self, form):
        received_csrf_token = self.request.POST.get('csrfmiddlewaretoken')
        print(f"Received CSRF Token: {received_csrf_token}")

        # Your existing logic to save the form data
        return super().form_valid(form)

class OpinionsForm(SuccessMessageMixin, generic.CreateView):
    template_name = 'opinions_form.html'
    model = models.Opinions
    fields = ['name', 'email', 'cruise', 'opinion']
    success_url = reverse_lazy('opinions_info')
    success_message = 'Thank you, %(name)s! Your opinion has been recorded!'

    def form_valid(self, form):
        received_csrf_token = self.request.POST.get('csrfmiddlewaretoken')
        print(f"Received CSRF Token: {received_csrf_token}")

        # Your existing logic to save the form data
        return super().form_valid(form)
