from django import forms

from models import Cluster

class IndexForm(forms.Form):
    cluster = forms.ModelChoiceField(required=False, label='Cluster', queryset=Cluster.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    # query = forms.CharField(required=False, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search' }))
