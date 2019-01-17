from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from datetime import date
from django.core.exceptions import ValidationError

from .models import Hurtownie, Poczta, Magazyny, Pracownicy
from .forms import AddMagazine, AddWorker

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect(hurtownia)
    else:
        return render(request, 'shop/index.html')

def hurtownia(request, hurtownia_id=1):
    if not request.user.is_authenticated:
        return redirect(index)

    else:
        hurtownia = get_object_or_404(Hurtownie, pk=hurtownia_id)
        return render(request, 'shop/hurtownia.html', {'hurtownia': hurtownia})

def user_login(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(hurtownia)

    else:
        return redirect(index)

def logout_view(request):
    logout(request)
    return redirect(index)

def magazines(request, magazyny=Magazyny.objects.all()):
    if not request.user.is_authenticated:
        return redirect(index)
    return render(request, 'shop/magazines.html', {'magazyny':magazyny})

def filter_magazines(request):
    query = request.GET.get('search')
    if query:
        result = Magazyny.objects.filter(miejscowosc__icontains=query) | Magazyny.objects.filter(ulica__icontains=query) |\
                 Magazyny.objects.filter(nr_budynku__iexact=query) | Magazyny.objects.filter(nr_lokalu__iexact=query) | \
                 Magazyny.objects.filter(powierzchnia__iexact=query)

        return render(request, 'shop/magazines.html', {'magazyny':result})

def add_magazine(request):
    return render(request, 'shop/add_magazine.html')

def post_magazine(request):
    if request.method == 'POST':
        form = AddMagazine(request.POST)
        if form.is_valid():
            id_magazynu = Magazyny.objects.aggregate(Max('id_magazynu')).get("id_magazynu__max") + 1
            miejscowosc = form.cleaned_data['miejscowosc']
            ulica = form.cleaned_data['ulica']
            nr_budynku = form.cleaned_data['nr_budynku']
            nr_lokalu = form.cleaned_data['nr_lokalu']
            powierzchnia = form.cleaned_data['powierzchnia']
            id_hurtowni = Hurtownie.objects.all().first()
            id_poczty = Poczta.objects.all().first()
            magazyn = Magazyny(id_magazynu=id_magazynu, miejscowosc=miejscowosc, ulica=ulica, nr_budynku=nr_budynku, nr_lokalu=nr_lokalu,
                               powierzchnia=powierzchnia, id_hurtowni=id_hurtowni, id_poczty=id_poczty)
            magazyn.save()

            return redirect(magazines)

def magazine_details(request, id_magazynu):
    magazyn = Magazyny.objects.get(id_magazynu__iexact=id_magazynu)
    return render(request, 'shop/magazine_details.html', {'magazyn':magazyn, 'id_magazynu':id_magazynu})

def delete_magazine(request, id_magazynu):
    Magazyny.objects.filter(id_magazynu__iexact=id_magazynu).delete()
    return redirect(magazines)

def update_magazine(request, id_magazynu):
    if request.method == 'POST':
        form = AddMagazine(request.POST)
        if form.is_valid():
            miejscowosc = form.cleaned_data['miejscowosc']
            ulica = form.cleaned_data['ulica']
            nr_budynku = form.cleaned_data['nr_budynku']
            nr_lokalu = form.cleaned_data['nr_lokalu']
            powierzchnia = form.cleaned_data['powierzchnia']
            Magazyny.objects.filter(id_magazynu__iexact=id_magazynu).update(miejscowosc=miejscowosc, ulica=ulica, nr_budynku=nr_budynku, nr_lokalu=nr_lokalu,
                                                                            powierzchnia=powierzchnia)

            return redirect(magazines)

    else:
        return redirect(add_magazine)

def workers(request, pracownicy=Pracownicy.objects.all()):
    if not request.user.is_authenticated:
        return redirect(index)
    return render(request, 'shop/workers.html', {'pracownicy':pracownicy})

def filter_workers(request):
    query = request.GET.get('search')
    if query:
        result = Pracownicy.objects.filter(miejscowosc__icontains=query) | Pracownicy.objects.filter(ulica__icontains=query) |\
                 Pracownicy.objects.filter(nr_budynku__iexact=query) | Pracownicy.objects.filter(nr_lokalu__iexact=query) | \
                 Pracownicy.objects.filter(imie__iexact=query) | Pracownicy.objects.filter(nazwisko__icontains=query) |\
                 Pracownicy.objects.filter(pesel__icontains=query) | Pracownicy.objects.filter(adres_e_mail__icontains=query) |\
                 Pracownicy.objects.filter(nr_telefonu__icontains=query)

        return render(request, 'shop/workers.html', {'pracownicy':result})

def add_worker(request):
    return render(request, 'shop/add_worker.html')

def post_worker(request):
    if request.method == 'POST':
        form = AddWorker(request.POST)
        if form.is_valid():
            id_pracownika = Pracownicy.objects.aggregate(Max('id_pracownika')).get("id_pracownika__max") + 1
            imie = form.cleaned_data['imie']
            nazwisko = form.cleaned_data['nazwisko']
            pesel = form.cleaned_data['pesel']
            miejscowosc = form.cleaned_data['miejscowosc']
            ulica = form.cleaned_data['ulica']
            nr_budynku = form.cleaned_data['nr_budynku']
            nr_lokalu = form.cleaned_data['nr_lokalu']
            data_urodzenia = form.cleaned_data['data_urodzenia']
            adres_e_mail= form.cleaned_data['adres_e_mail']
            nr_telefonu = form.cleaned_data['nr_telefonu']
            stanowisko = form.cleaned_data['stanowisko']
            data_zatrudnienia = date.today()
            pracownik = Pracownicy(id_pracownika=id_pracownika, miejscowosc=miejscowosc, ulica=ulica, nr_budynku=nr_budynku, nr_lokalu=nr_lokalu,
                                   imie=imie, nazwisko=nazwisko, pesel=pesel, data_urodzenia=data_urodzenia, adres_e_mail=adres_e_mail,
                                   nr_telefonu=nr_telefonu, stanowisko=stanowisko, data_zatrudniena=data_zatrudnienia,
                                   id_hurtowni=1, id_poczty=1)
            pracownik.save()

            return redirect(workers)

    else:
        return redirect(add_worker)


def worker_details(request, id_pracownika):
    pracownik = Pracownicy.objects.get(id_pracownika__iexact=id_pracownika)
    return render(request, 'shop/worker_details.html', {'pracownik':pracownik, 'id_pracownika':id_pracownika})

def delete_worker(request, id_pracownika):
    Pracownicy.objects.filter(id_pracownika__iexact=id_pracownika).delete()
    return redirect(workers)

def update_worker(request, id_pracownika):
    if request.method == 'POST':
        form = AddWorker(request.POST)
        print(form)
        if form.is_valid():
            imie = form.cleaned_data['imie']
            nazwisko = form.cleaned_data['nazwisko']
            pesel = form.cleaned_data['pesel']
            miejscowosc = form.cleaned_data['miejscowosc']
            ulica = form.cleaned_data['ulica']
            nr_budynku = form.cleaned_data['nr_budynku']
            nr_lokalu = form.cleaned_data['nr_lokalu']
            data_urodzenia = form.cleaned_data['data_urodzenia']
            adres_e_mail = form.cleaned_data['adres_e_mail']
            nr_telefonu = form.cleaned_data['nr_telefonu']
            stanowisko = form.cleaned_data['stanowisko']
            Pracownicy.objects.filter(id_pracownika__iexact=id_pracownika).update(imie=imie, nazwisko=nazwisko, pesel=pesel,
                                                                                  data_urodzenia=data_urodzenia, miejscowosc=miejscowosc,
                                                                                  ulica=ulica, nr_budynku=nr_budynku, nr_lokalu=nr_lokalu,
                                                                                  adres_e_mail=adres_e_mail, nr_telefonu=nr_telefonu, stanowisko=stanowisko)

            return redirect(workers)

def goods(request):
    return render(request, 'shop/goods.html')