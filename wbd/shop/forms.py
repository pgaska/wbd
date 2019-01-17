from django import forms

class AddMagazine(forms.Form):
    miejscowosc = forms.CharField(max_length=30)
    ulica = forms.CharField(max_length=40, required=False)
    nr_budynku = forms.CharField(max_length=4)
    nr_lokalu = forms.CharField(max_length=4, required=False)
    powierzchnia = forms.FloatField()

class AddWorker(forms.Form):
    imie = forms.CharField(max_length=20)
    nazwisko = forms.CharField(max_length=40)
    miejscowosc = forms.CharField(max_length=30)
    ulica = forms.CharField(max_length=40, required=False)
    nr_budynku = forms.CharField(max_length=4)
    nr_lokalu = forms.CharField(max_length=4, required=False)
    pesel = forms.CharField(max_length=11, required=False)
    data_urodzenia = forms.DateField()
    stanowisko = forms.CharField(max_length=30)
    adres_e_mail = forms.CharField(max_length=50)
    nr_telefonu = forms.CharField(max_length=15)