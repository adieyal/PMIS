from django import forms

from models import Cluster

years = (
    (2015, 2015),
    (2014, 2014),
    (2013, 2013),
)

class IndexForm(forms.Form):
    cluster = forms.ModelChoiceField(required=False, label='Cluster', queryset=Cluster.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    # query = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search' }))

class NewIndexForm(forms.Form):
    cluster = forms.ModelChoiceField(required=False, label='Cluster', queryset=Cluster.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    fin_year = forms.ChoiceField(required=False, choices=years, widget=forms.Select(attrs={'class': 'form-control'}))
    exclude_previous = forms.BooleanField(required=False)
    # query = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search' }))
