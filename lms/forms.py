from django import forms
from lms.models import Question,Answer,ContactUs,OnlineClassroom,GetMoreInfo
from django.forms import ModelForm
from django.utils.text import slugify

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['question']

class GetInfoForm(forms.ModelForm):
	class Meta:
		model = GetMoreInfo
		exclude = ['course']
		widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }

class ContactUsForm(forms.ModelForm):
	class Meta:
		model = ContactUs
		fields = '__all__'

def get_my_choices(course_id):
	batches = [(i.id,i.batch) for i in OnlineClassroom.objects.filter(course_id = course_id)]
	return batches

class OnlineForm(forms.Form):
	batch = forms.CharField()

	def __init__(self, *args, **kwargs):
			course_id = kwargs.pop('course_id')
			super().__init__(*args, **kwargs)
			self.fields['batch'] = forms.ChoiceField(choices=get_my_choices(course_id),widget=forms.RadioSelect())


class EnrolForm(forms.Form):
	email = forms.EmailField()
	mobile = forms.IntegerField()