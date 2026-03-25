from django.shortcuts import render

# Create your views here.
import random
import string

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.shortcuts import redirect, render

from .forms import AvailabilityInputForm, EventForm, JoinEventForm
from .models import Availability, Event, EventMembership, Notification


def home(request):
    return render(request, 'planner/home.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('create_event')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created. Welcome to Time Match!')
            return redirect('create_event')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def _generate_event_code():
    chars = string.ascii_uppercase + string.digits
    for _ in range(20):
        code = ''.join(random.choices(chars, k=6))
        if not Event.objects.filter(code=code).exists():
            return code
    raise RuntimeError('Could not generate unique event code')


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            event.code = _generate_event_code()
            event.save()

            EventMembership.objects.get_or_create(user=request.user, event=event)
            Notification.objects.create(
                user=request.user,
                event=event,
                message=f'Event created: {event.title} (code: {event.code})',
            )
            messages.success(request, f'Event created. Share code {event.code} with your friends.')
            return redirect('create_event')
    else:
        form = EventForm()

    user_events = Event.objects.filter(memberships__user=request.user).distinct()
    return render(request, 'planner/create_event.html', {'form': form, 'user_events': user_events})


@login_required
def join_event(request):
    if request.method == 'POST':
        form = JoinEventForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].strip().upper()
            try:
                event = Event.objects.get(code=code)
            except Event.DoesNotExist:
                messages.error(request, 'Event code not found.')
            else:
                membership, created = EventMembership.objects.get_or_create(user=request.user, event=event)
                if created:
                    messages.success(request, f'Successfully joined event: {event.title}')
                else:
                    messages.info(request, f'You are already member of: {event.title}')
                return redirect('join_event')
    else:
        form = JoinEventForm()

    user_events = Event.objects.filter(memberships__user=request.user).distinct()
    return render(request, 'planner/join_event.html', {'form': form, 'user_events': user_events})


@login_required
def availability_input(request):
    if request.method == 'POST':
        form = AvailabilityInputForm(request.POST, user=request.user)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.user = request.user
            availability.save()
            messages.success(request, 'Availability submitted!')
            return redirect('availability_input')
    else:
        form = AvailabilityInputForm(user=request.user)

    user_events = Event.objects.filter(memberships__user=request.user).distinct()
    return render(request, 'planner/availability_input.html', {'form': form, 'user_events': user_events})


@login_required
def event_overview(request):
    user_events = Event.objects.filter(memberships__user=request.user).distinct()
    context = {'user_events': user_events}
    return render(request, 'planner/event_overview.html', context)


@login_required
def notification_panel(request):
    notifications = Notification.objects.filter(user=request.user)
    context = {'notifications': notifications}
    return render(request, 'planner/notification_panel.html', context)