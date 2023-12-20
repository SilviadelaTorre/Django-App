from django.shortcuts import render, HttpResponse
from django.urls import reverse_lazy
from . import models
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.csrf import csrf_protect
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def destinations(request):
    all_destinations = models.Destination.objects.all()
    return render(request, 'destinations.html', { 'destinations': all_destinations})


def cruise_opinions_table(request):
    cruises_and_opinions = {
        'cruises': models.Cruise.objects.all(),
        'opinions': models.Opinions.objects.all(),
    }
    return render(request, 'opinions_info.html', {'opinions': cruises_and_opinions})

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

    '''def form_valid(self, form):
        received_csrf_token = self.request.POST.get('csrfmiddlewaretoken')
        print(f"Received CSRF Token: {received_csrf_token}")

        # Your existing logic to save the form data
        return super().form_valid(form)'''
    

class Opinions(SuccessMessageMixin, generic.CreateView): # form opinions
    template_name = 'opinions.html'
    model = models.Opinions
    fields = ['name', 'email', 'cruise', 'opinion']
    success_url = reverse_lazy('opinions_info')
    success_message = 'Thank you, %(name)s! Your opinion has been saved!'

    def form_valid(self, form):
        received_csrf_token = self.request.POST.get('csrfmiddlewaretoken')
        print(f"Received CSRF Token: {received_csrf_token}")
        return super().form_valid(form)

class OpinionsTable(SuccessMessageMixin, generic.CreateView):
    template_name = 'opinions_info.html'
    model = models.Opinions
    context_object_name = 'opinion'