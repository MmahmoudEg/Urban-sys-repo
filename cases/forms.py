from django import forms
from .models import Case, Client, Lawyer
from .models import Document
from django.forms import inlineformset_factory
from file_resubmit.widgets import ResubmitFileWidget


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Existing document
            self.fields['file'].required = False
            self.fields['file'].widget.attrs['class'] = 'form-control-file optional-file'

# DocumentFormSet = inlineformset_factory(
#     Case,
#     Document,
#     form=DocumentForm,
#     extra=1,
#     can_delete=True,
#     fields=('title', 'file')
# )  

DocumentFormSet = inlineformset_factory(
    Case,
    Document,
    fields=('title', 'file'),
    extra=1,
    can_delete=True,
    widgets={
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    }
)

class CaseForm(forms.ModelForm):
    attachment = forms.FileField(widget=ResubmitFileWidget, required=False)
    class Meta:
        model = Case
        fields = ['case_number','court','case_type','title', 'client', 'lawyer', 'status',  'description']



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone']
        # template_name = 'clients/client_form.html'


class LawyerForm(forms.ModelForm):
    class Meta:
        model = Lawyer
        fields = ['first_name', 'last_name', 'email', 'phone']
        # template_name = 'lawyers/lawyer_form.html'

# Add to forms.py
from .models import Hearing

class HearingForm(forms.ModelForm):
    class Meta:
        model = Hearing
        fields = ('hearing_date', 'notes')

HearingFormSet = inlineformset_factory(
    Case,
    Hearing,
    fields=('hearing_date', 'notes'),
    extra=1,
    can_delete=True,
    widgets={
        'hearing_date': forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            },
            format='%Y-%m-%dT%H:%M'
        ),
        'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    }
)