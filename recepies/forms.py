from django import forms


class SearchForm(forms.Form):
    word = forms.CharField(label='', max_length=100, min_length=0)
