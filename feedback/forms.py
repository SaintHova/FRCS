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
            'class': 'transition w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-200 h-32 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 ease-in-out',


        }
	))

    class Meta:
        model = Feedback
        fields = ['first_name', 'team_num', 'message']
