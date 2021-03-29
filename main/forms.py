from django import forms


class SeoRequestForm(forms.Form):
	keyword = forms.CharField(label='Keyword',
	                          max_length=100,
	                          widget=forms.TextInput(attrs={'placeholder': 'Keyword (Any)'}))
	engine = forms.CharField(label='Engine',
	                         max_length=100,
	                         widget=forms.TextInput(attrs={'placeholder': 'Search Engine(Google, Yandex etc..)'}))
	location = forms.CharField(label='Location',
	                           max_length=100,
	                           widget=forms.TextInput(attrs={'placeholder': 'Location (Country)'}))
