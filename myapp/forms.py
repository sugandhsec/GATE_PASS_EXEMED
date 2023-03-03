from django import forms
from .models import Rgp_entry
from .models import Nrgp_entry


# creating a form
class Rgp_entryForm(forms.ModelForm):




	# create meta class
	class Meta:
	
		# specify model to be used
		model = Rgp_entry
		# model = Nrgp_entry

		# specify fields to be used
		fields = '__all__'

class Nrgp_entryForm(forms.ModelForm):




	# create meta class
	class Meta:
	
		# specify model to be used
		# model = Rgp_entry
		model = Nrgp_entry

		# specify fields to be used
		fields = '__all__'