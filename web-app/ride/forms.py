from django import forms
from .models import Ride
from .models import Share

class RideCreationForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['des', 'start_date', 'arrive_date', 'pas_num', 'share_valid', 'share_max_num']

        start_date = forms.DateField(
            widget = forms.DateInput(
                attrs= {
                        'type':'date',
                        }
            )
        )

class SharePickForm(forms.ModelForm):
    class Meta:
        model = Share
        fields = ['des', 'start_date_0', 'start_date_1', 'arrive_date_0', 'arrive_date_1', 'pas_num']

class ShareUpdateForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['share_number']
