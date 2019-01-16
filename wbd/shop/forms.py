from django import forms

class AddMagazine(forms.Form):
    miejscowosc = forms.CharField(max_length=30)
    ulica = forms.CharField(max_length=40, required=False)
    nr_budynku = forms.CharField(max_length=4)
    nr_lokalu = forms.CharField(max_length=4, required=False)
    powierzchnia = forms.FloatField()