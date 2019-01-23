from django import forms

class AddMagazine(forms.Form):
    miejscowosc = forms.CharField(max_length=30)
    ulica = forms.CharField(max_length=40, required=False)
    nr_budynku = forms.CharField(max_length=4)
    nr_lokalu = forms.CharField(max_length=4, required=False)
    powierzchnia = forms.FloatField()
    kod_pocztowy = forms.CharField(max_length=6, required=False)

class AddWorker(forms.Form):
    imie = forms.CharField(max_length=20)
    nazwisko = forms.CharField(max_length=40)
    miejscowosc = forms.CharField(max_length=30)
    ulica = forms.CharField(max_length=40, required=False)
    nr_budynku = forms.CharField(max_length=4)
    nr_lokalu = forms.CharField(max_length=4, required=False)
    kod_pocztowy = forms.CharField(max_length=6, required=False)
    pesel = forms.CharField(max_length=11, required=False)
    data_urodzenia = forms.DateField()
    stanowisko = forms.CharField(max_length=30)
    adres_e_mail = forms.CharField(max_length=50)
    nr_telefonu = forms.CharField(max_length=15)

class ChooseType(forms.Form):
    typ = forms.CharField(max_length=20)

class AddProcesor(forms.Form):
    produent = forms.CharField(max_length=60)
    kod_producenta = forms.CharField(max_length=20)
    model = forms.CharField(max_length=20, required=False)
    cena = forms.DecimalField(max_digits=10, decimal_places=2)
    liczba_rdzeni = forms.IntegerField()
    taktowanie = forms.FloatField()
    magazyn = forms.CharField(max_length=100)

class AddPamiec(forms.Form):
    produent = forms.CharField(max_length=60)
    kod_producenta = forms.CharField(max_length=20)
    model = forms.CharField(max_length=20, required=False)
    cena = forms.DecimalField(max_digits=10, decimal_places=2)
    typ = forms.CharField(max_length=4)
    pojemnosc = forms.IntegerField()
    magazyn = forms.CharField(max_length=100)

class AddPlytaGlowna(forms.Form):
    produent = forms.CharField(max_length=60)
    kod_producenta = forms.CharField(max_length=20)
    model = forms.CharField(max_length=20, required=False)
    cena = forms.DecimalField(max_digits=10, decimal_places=2)
    chipset = forms.CharField(max_length=15)
    standard_pamieci = forms.CharField(max_length=4)
    magazyn = forms.CharField(max_length=100)

class AddKartaGraficzna(forms.Form):
    produent = forms.CharField(max_length=60)
    kod_producenta = forms.CharField(max_length=20)
    model = forms.CharField(max_length=20, required=False)
    cena = forms.DecimalField(max_digits=10, decimal_places=2)
    ilosc_pamieci = forms.IntegerField()
    rodzaj_pamieci = forms.CharField(max_length=5)
    szyna = forms.IntegerField()
    magazyn = forms.CharField(max_length=100)

class AddSalary(forms.Form):
    kwota = forms.FloatField()
    premia = forms.FloatField()