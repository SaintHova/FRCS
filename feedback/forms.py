from django import forms
from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
		attrs={
            
            'class': 'form-single',


        }
	))
    team_num = forms.IntegerField(label='Last Name', widget=forms.NumberInput(
		attrs={
            'class': 'form-single',


        }
	))
    message = forms.CharField(label='Message', widget=forms.Textarea(
		attrs={
            'class': 'h-32 form-single',


        }
	))

    class Meta:
        model = Feedback
        fields = ['first_name', 'team_num', 'message']
