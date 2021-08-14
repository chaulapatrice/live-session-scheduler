from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import (
    AddExpertForm,
    SelectExpertForm,
    PickDatesForm,
    DateTimeConfirmationForm
    )
from .models import Event, Expert
from uuid import uuid4
from django.core.mail import send_mail
from .utils import get_month_number
from django.utils.timezone import datetime
# Create your views here.
@login_required(login_url='accounts/login')
def select_expert(request):
    form = SelectExpertForm()
    experts = Expert.objects.all()

    if request.method == 'POST':
        form = SelectExpertForm(request.POST)
        if form.is_valid():
            # Create the event
            cd = form.cleaned_data
            expert = Expert.objects.get(pk=cd['expert_id'])
            event = Event.objects.create(
                user=request.user,
                expert=expert,
                slug=uuid4()
            )
            return redirect("core:pick_dates",
                     event_slug=event.slug)

    return render(request, "core/select_expert.html", {
        'form': form,
        'experts': experts,
    })

def pick_dates(request, event_slug):
    form = PickDatesForm()
    event = Event.objects.get(slug=event_slug)
    if request.method == "POST":
        form = PickDatesForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # generate three links and send them
            link_1 = 'http://' + request.get_host() + reverse("core:confirm_date",kwargs={
                'event_slug': event.slug,
                'date': cd['date_1'],
                'time': cd['time_1']
            })
            link_2 = 'http://' + request.get_host() +  reverse("core:confirm_date",kwargs={
                'event_slug': event.slug,
                'date': cd['date_2'],
                'time': cd['time_2']
            })
            link_3 = 'http://' + request.get_host() +  reverse("core:confirm_date",kwargs={
                'event_slug': event.slug,
                'date': cd['date_3'],
                'time': cd['time_3']
            })


            alternative_link = 'http://' + request.get_host() +  reverse("core:pick_dates", kwargs={'event_slug': event.slug})

            message =(
            f"""
                 Hi, Good day to you.
                 Confirm which of the following dates are you available for a live session.
                 {cd['date_1']} at { cd['time_1']}
                 {link_1}

                 {cd['date_2']} at { cd['time_2']}
                 {link_2}

                 {cd['date_3']} at { cd['time_3']}
                 {link_3}

                 If none of the above suit you, select three 3 different dates that suit you.
                 {alternative_link}
                """)
            email_to  = event.expert.email if request.user.is_authenticated else event.expert.user
            send_mail(
                'Live session schedule',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email_to],
                fail_silently=False
            )

            return redirect('core:sending_successful')

    return render(request, "core/pick_dates.html", {
        'form': form
    })


def sending_successful(request):
    return render(request, "core/sending_successful.html", {})

def confirm_date(request, event_slug, date, time):

    event = Event.objects.get(slug=event_slug)

    data = {
        'date': date,
        'time': time,
    }
    form = DateTimeConfirmationForm(data)

    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data

            # Get the year, month, day from date field
            date_values = cd['date'].split(' ')
            month = get_month_number(date_values[0])
            day = date_values[1].strip(',')
            day = int(day)
            year = int(date_values[2])

            # Get hour and minute from time field
            time_values = cd['time'].strip(' PM').split(':')
            hour = int(time_values[0])
            minute = int(time_values[1])

            # Create the date
            event.date = datetime(year, month, day, hour, minute)
            event.scheduled = True
            event.save()
            event.refresh_from_db()

            # Send email to both parties
            link = 'http://' + request.get_host() + reverse(
                'core:view_event', kwargs={'event_slug': event.slug})
            message = (
                f"""
                Your live session has been successfully scheduled on {event.date}.
                Use the following link to join.
                {link}
                """
            )

            send_mail(
                'Live session has been scheduled',
                message,
                settings.DEFAULT_FROM_EMAIL,
                [event.expert.email, event.user.email],
                fail_silently=False
            )

            return redirect(
                'core:date_confirmed',
                event_slug=event.slug)


    return render(request,"core/confirm_date.html", {
        'event_slug': event.slug,
    })

def date_confirmed(request, event_slug):
    return render(request, "core/date_confirmed.html", {})

def view_event(request, event_slug):
    event = Event.objects.get(slug=event_slug)
    return render(request, "core/view_event.html", {
        'event': event
    })

def add_expert(request):
    form = AddExpertForm()

    if request.method == "POST":
        form = AddExpertForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:select_expert')

    return render(request, "core/add_expert.html", {
        'form': form
    })
