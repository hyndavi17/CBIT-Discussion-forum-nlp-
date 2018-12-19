from django.forms import ModelForm
from django import forms
from discussion.models import comments
class CommentForm(forms.ModelForm):
	class Meta:
		model=comments
		exclude=()