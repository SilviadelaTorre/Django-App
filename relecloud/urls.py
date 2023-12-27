## APP (Relecloud)

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('destinations/', views.destinations, name='destinations'),
    path('destination/<int:pk>', views.DestinationDetailView.as_view(), name='destination_detail' ),
    path('cruise/<int:pk>', views.CruiseDetailView.as_view(), name='cruise_detail'),
    path('info_request', views.InfoRequestCreate.as_view(), name='info_request'),
    path('email_notification', views.email_notification, name='email_notification'),
    path('opinions/', views.grouped_opinions, name='opinions_info'),
    path('opinions/form', views.OpinionsForm.as_view(), name='opinions_form')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

