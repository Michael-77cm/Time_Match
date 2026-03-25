from django import forms
from .models import Availability, Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title']


class JoinEventForm(forms.Form):
    code = forms.CharField(max_length=8, label='Event code')


class AvailabilityInputForm(forms.ModelForm):
    event = forms.ModelChoiceField(queryset=Event.objects.none(), label='Event title')

    class Meta:
        model = Availability
        fields = ['event', 'date', 'start_time', 'end_time', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['event'].queryset = Event.objects.filter(memberships__user=user).distinct()