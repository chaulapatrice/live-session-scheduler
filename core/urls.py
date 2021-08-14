from django .urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('add-expert/', views.add_expert, name="add_expert"),
    path('', views.select_expert, name='select_expert'),
    path('pick-dates/<slug:event_slug>/', views.pick_dates, name='pick_dates'),
    path('confirm-date/<slug:event_slug>/<str:date>/<str:time>/',
          views.confirm_date, name='confirm_date'),
    path('date-confirmed/<slug:event_slug>/',
          views.date_confirmed, name='date_confirmed'),
    path('sending-successful/', views.sending_successful, name="sending_successful"),
    path("view-event/<slug:event_slug>/", views.view_event, name="view_event"),
]