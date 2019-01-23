from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max
from django.db import transaction
from datetime import date
from django.core.exceptions import ValidationError

from .models import Hurtownie, Poczta, Magazyny, Pracownicy, Procesor, PlytaGlowna, Pamiec, KartaGraficzna, Towary, Wynagrodzenia
from .forms import AddMagazine, AddWorker, ChooseType, AddKartaGraficzna, AddPamiec, AddPlytaGlowna, AddProcesor, AddSalary

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

def magazines(request):
    magazyny=Magazyny.objects.all()
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
            if not Magazyny.objects.all():
                id_magazynu = 1
            else:
                id_magazynu = Magazyny.objects.aggregate(Max('id_magazynu')).get("id_magazynu__max") + 1
            miejscowosc = form.cleaned_data['miejscowosc']
            ulica = form.cleaned_data['ulica']
            nr_budynku = form.cleaned_data['nr_budynku']
            nr_lokalu = form.cleaned_data['nr_lokalu']
            powierzchnia = form.cleaned_data['powierzchnia']
            id_hurtowni = Hurtownie.objects.all().first()
            kod_pocztowy = form.cleaned_data['kod_pocztowy']
            id_poczty = Poczta.objects.aggregate(Max('id_poczty')).get("id_poczty__max") + 1
            poczta = Poczta(id_poczty=id_poczty, kod_pocztowy=kod_pocztowy, miasto=miejscowosc)
            poczta.save()
            magazyn = Magazyny(id_magazynu=id_magazynu, miejscowosc=miejscowosc, ulica=ulica, nr_budynku=nr_budynku, nr_lokalu=nr_lokalu,
                               powierzchnia=powierzchnia, id_hurtowni=id_hurtowni, id_poczty=poczta)
            magazyn.save()
            transaction.commit('default')

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
            kod_pocztowy = form.cleaned_data['kod_pocztowy']
            id_poczty = Poczta.objects.aggregate(Max('id_poczty')).get("id_poczty__max") + 1
            poczta = Poczta(id_poczty=id_poczty, kod_pocztowy=kod_pocztowy, miasto=miejscowosc)
            poczta.save()
            Magazyny.objects.filter(id_magazynu__iexact=id_magazynu).update(miejscowosc=miejscowosc, ulica=ulica, nr_budynku=nr_budynku, nr_lokalu=nr_lokalu,
                                                                            powierzchnia=powierzchnia, id_poczty=poczta)
            transaction.commit('default')

            return redirect(magazines)

    else:
        return redirect(add_magazine)

def magazine_goods(request, id_magazynu):
    magazyn = get_object_or_404(Magazyny, pk=id_magazynu)
    procesory = Procesor.objects.all()
    pamiec = Pamiec.objects.all()
    karty_graficzne = KartaGraficzna.objects.all()
    plyty_glowne = PlytaGlowna.objects.all()
    towary = []
    for procesor in procesory:
        towar = Towary.objects.filter(pk=procesor.id_towaru, id_magazynu=magazyn).first()
        towary.append(towar)

    for p in pamiec:
        towar = Towary.objects.filter(pk=p.id_towaru, id_magazynu=magazyn).first()
        towary.append(towar)

    for karta_graficzna in karty_graficzne:
        towar = Towary.objects.filter(pk=karta_graficzna.id_towaru, id_magazynu=magazyn).first()
        towary.append(towar)

    for plyta_glowna in plyty_glowne:
        towar =Towary.objects.filter(pk=plyta_glowna.id_towaru, id_magazynu=magazyn).first()
        towary.append(towar)
    print(towary)
    return render(request, 'shop/magazine_goods.html', {'magazyn':magazyn, 'towary':towary})

def filter_magazine_goods(request, id_magazynu):
    magazyn = get_object_or_404(Magazyny, pk=id_magazynu)
    query = request.GET.get('search')
    if query:
        result = Towary.objects.filter(produent__icontains=query, id_magazynu=magazyn) | Towary.objects.filter(
                  kod_producenta__iexact=query,id_magazynu=magazyn) | \
                  Towary.objects.filter(model__icontains=query,id_magazynu=magazyn) | Towary.objects.filter(cena__iexact=query,id_magazynu=magazyn)
        transaction.commit('default')

        return render(request, 'shop/magazine_goods.html', {'magazyn':magazyn, 'towary': result})

def workers(request):
    pracownicy = Pracownicy.objects.all()
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
            if not Pracownicy.objects.all():
                id_pracownika = 1
            else:
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
            kod_pocztowy = form.cleaned_data['kod_pocztowy']
            data_zatrudnienia = date.today()
            id_poczty = Poczta.objects.aggregate(Max('id_poczty')).get("id_poczty__max") + 1
            poczta = Poczta(id_poczty=id_poczty, kod_pocztowy=kod_pocztowy, miasto=miejscowosc)
            poczta.save()
            pracownik = Pracownicy(id_pracownika=id_pracownika, miejscowosc=miejscowosc, ulica=ulica, nr_budynku=nr_budynku, nr_lokalu=nr_lokalu,
                                   imie=imie, nazwisko=nazwisko, pesel=pesel, data_urodzenia=data_urodzenia, adres_e_mail=adres_e_mail,
                                   nr_telefonu=nr_telefonu, stanowisko=stanowisko, data_zatrudniena=data_zatrudnienia,
                                   id_hurtowni=1, id_poczty=id_poczty)
            pracownik.save()
            transaction.commit('default')

            return redirect(workers)

        else:
            return redirect(add_worker)


def worker_details(request, id_pracownika):
    pracownik = get_object_or_404(Pracownicy, pk=id_pracownika)
    poczta = get_object_or_404(Poczta, id_poczty__iexact=pracownik.id_poczty)
    return render(request, 'shop/worker_details.html', {'pracownik':pracownik, 'id_pracownika':id_pracownika, 'poczta':poczta})

def delete_worker(request, id_pracownika):
    Pracownicy.objects.filter(id_pracownika__iexact=id_pracownika).delete()
    return redirect(workers)

def update_worker(request, id_pracownika):
    if request.method == 'POST':
        form = AddWorker(request.POST)
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
            kod_pocztowy = form.cleaned_data['kod_pocztowy']
            id_poczty = Poczta.objects.aggregate(Max('id_poczty')).get("id_poczty__max") + 1
            poczta = Poczta(id_poczty=id_poczty, kod_pocztowy=kod_pocztowy, miasto=miejscowosc)
            poczta.save()
            Pracownicy.objects.filter(id_pracownika__iexact=id_pracownika).update(imie=imie, nazwisko=nazwisko, pesel=pesel,
                                                                                  data_urodzenia=data_urodzenia, miejscowosc=miejscowosc,
                                                                                  ulica=ulica, nr_budynku=nr_budynku, nr_lokalu=nr_lokalu,
                                                                                  adres_e_mail=adres_e_mail, nr_telefonu=nr_telefonu, stanowisko=stanowisko,
                                                                                  id_poczty=id_poczty)
            transaction.commit('default')

            return redirect(workers)

def salaries(request, id_pracownika):
    pracownik = get_object_or_404(Pracownicy, pk=id_pracownika)
    wynagrodzenia = Wynagrodzenia.objects.filter(id_pracownika=pracownik.id_pracownika)
    print(wynagrodzenia)
    return render(request, 'shop/salaries.html', {'pracownik':pracownik, 'wynagrodzenia':wynagrodzenia})

def post_salary(request, id_pracownika):
    if request.method == "POST":
        form = AddSalary(request.POST)
        if form.is_valid():
            kwota = form.cleaned_data['kwota']
            premia = form.cleaned_data['premia']
            if not Wynagrodzenia.objects.all():
                id_wynagrodzenia = 1
            else:
                id_wynagrodzenia = Wynagrodzenia.objects.aggregate(Max('id_wynagrodzenia')).get("id_wynagrodzenia__max") + 1
            wynagrodzenie = Wynagrodzenia(id_wynagrodzenia=id_wynagrodzenia, kwota=kwota,
                                          premia=premia, id_pracownika=id_pracownika,
                                          data=date.today())
            wynagrodzenie.save()
            transaction.commit('default')

            return redirect(salaries, id_pracownika=id_pracownika)

def goods(request):
    procesory = Procesor.objects.all()
    pamiec = Pamiec.objects.all()
    karty_graficzne = KartaGraficzna.objects.all()
    plyty_glowne = PlytaGlowna.objects.all()
    towary=[]
    for procesor in procesory:
        towar = get_object_or_404(Towary, pk=procesor.id_towaru)
        towary.append(towar)

    for p in pamiec:
        towar = get_object_or_404(Towary, pk=p.id_towaru)
        towary.append(towar)

    for karta_graficzna in karty_graficzne:
        towar = get_object_or_404(Towary, pk=karta_graficzna.id_towaru)
        towary.append(towar)

    for plyta_glowna in plyty_glowne:
        towar = get_object_or_404(Towary, pk=plyta_glowna.id_towaru)
        towary.append(towar)
    return render(request, 'shop/goods.html', {'towary':towary})

def filter_goods(request):
    query = request.GET.get('search')
    if query:
        result = Towary.objects.filter(produent__icontains=query) | Towary.objects.filter(kod_producenta__iexact=query) |\
                 Towary.objects.filter(model__icontains=query) | Towary.objects.filter(cena__iexact=query)
        transaction.commit('default')

        return render(request, 'shop/goods.html', {'towary':result})

def add_goods(request):
    return render(request, 'shop/add_goods.html')

def choose_type(request):
    if request.method == 'POST':
        form = ChooseType(request.POST)
        print(form)
        if form.is_valid():
            typ = form.cleaned_data['typ']
            if typ == 'Procesor':
                return redirect(add_procesor)
            elif typ == 'Pamięć':
                return redirect(add_pamiec)
            elif typ == 'Karta graficzna':
                return redirect(add_karta_graficzna)
            elif typ == 'Płyta główna':
                return redirect(add_plyta_glowna)

def add_procesor(request):
    return render(request, 'shop/add_procesor.html')

def add_karta_graficzna(request):
    return render(request, 'shop/add_karta_graficzna.html')

def add_pamiec(request):
    return render(request, 'shop/add_pamiec.html')

def add_plyta_glowna(request):
    return render(request, 'shop/add_plyta_glowna.html')

def post_procesor(request):
    if request.method == 'POST':
        form = AddProcesor(request.POST)
        if form.is_valid():
            if not Towary.objects.all():
                id_towaru = 1
            else:
                id_towaru = Towary.objects.aggregate(Max('id_towaru')).get('id_towaru__max') + 1
            producent = form.cleaned_data['produent']
            kod_producenta = form.cleaned_data['kod_producenta']
            model = form.cleaned_data['model']
            cena = form.cleaned_data['cena']
            id_magazynu = Magazyny.objects.all().first()
            towar = Towary(id_towaru=id_towaru, produent=producent, kod_producenta=kod_producenta,
                            model=model, cena=cena, id_magazynu=id_magazynu)
            towar.save()
            transaction.commit('default')

            if not Procesor.objects.all():
                id_procesora = 1
            else:
                id_procesora = Procesor.objects.aggregate(Max('id_procesora')).get('id_procesora__max') + 1
            liczba_rdzeni = form.cleaned_data['liczba_rdzeni']
            taktowanie = form.cleaned_data['taktowanie']
            procesor = Procesor(id_procesora=id_procesora, liczba_rdzeni=liczba_rdzeni, taktowanie=taktowanie, id_towaru=id_towaru)
            procesor.save()
            transaction.commit('default')

            return redirect(goods)

def post_pamiec(request):
    if request.method == 'POST':
        form = AddPamiec(request.POST)
        if form.is_valid():
            if not Towary.objects.all():
                id_towaru = 1
            else:
                id_towaru = Towary.objects.aggregate(Max('id_towaru')).get('id_towaru__max') + 1
            producent = form.cleaned_data['produent']
            kod_producenta = form.cleaned_data['kod_producenta']
            model = form.cleaned_data['model']
            cena = form.cleaned_data['cena']
            id_magazynu = Magazyny.objects.all().first()
            towar = Towary(id_towaru=id_towaru, produent=producent, kod_producenta=kod_producenta,
                           model=model, cena=cena,  id_magazynu=id_magazynu)
            towar.save()

            if not Pamiec.objects.all():
                id_pamieci = 1
            else:
                id_pamieci = Pamiec.objects.aggregate(Max('id_pamieci')).get('id_pamieci__max') + 1
            typ_ = form.cleaned_data['typ']
            pojemnosc = form.cleaned_data['pojemnosc']
            pamiec = Pamiec(id_pamieci=id_pamieci, typ=typ_, pojemnosc=pojemnosc, id_towaru=id_towaru)
            pamiec.save()

            return redirect(goods)

def post_plyta_glowna(request):
    if request.method == 'POST':
        form = AddPlytaGlowna(request.POST)
        if form.is_valid():
            if not Towary.objects.all():
                id_towaru = 1
            else:
                id_towaru = Towary.objects.aggregate(Max('id_towaru')).get('id_towaru__max') + 1
            producent = form.cleaned_data['produent']
            kod_producenta = form.cleaned_data['kod_producenta']
            model = form.cleaned_data['model']
            cena = form.cleaned_data['cena']
            id_magazynu = Magazyny.objects.all().first()
            towar = Towary(id_towaru=id_towaru, produent=producent, kod_producenta=kod_producenta,
                           model=model, cena=cena, id_magazynu=id_magazynu)
            towar.save()

            if not PlytaGlowna.objects.all():
                id_plyty_glownej = 1
            else:
                id_plyty_glownej = PlytaGlowna.objects.aggregate(Max('id_plyty_glownej')).get('id_plyty_glownej__max') + 1
            chipset = form.cleaned_data['chipset']
            standard_pamieci = form.cleaned_data['standard_pamieci']
            plyta_glowna = PlytaGlowna(id_plyty_glownej=id_plyty_glownej, chipset=chipset,
                                       standard_pamieci=standard_pamieci, id_towaru=id_towaru)
            plyta_glowna.save()

            return redirect(goods)

def post_karta_graficzna(request):
    if request.method == 'POST':
        form = AddKartaGraficzna(request.POST)
        print(form)
        if form.is_valid():
            if not Towary.objects.all():
                id_towaru = 1
            else:
                id_towaru = Towary.objects.aggregate(Max('id_towaru')).get('id_towaru__max') + 1
            producent = form.cleaned_data['produent']
            kod_producenta = form.cleaned_data['kod_producenta']
            model = form.cleaned_data['model']
            cena = form.cleaned_data['cena']
            id_magazynu = Magazyny.objects.all().first()
            towar = Towary(id_towaru=id_towaru, produent=producent, kod_producenta=kod_producenta,
                           model=model, cena=cena, id_magazynu=id_magazynu)
            towar.save()

            if not KartaGraficzna.objects.all():
                id_karty_graficznej = 1
            else:
                id_karty_graficznej = KartaGraficzna.objects.aggregate(Max('id_karty_graficznej')).get(
                'id_karty_graficznej__max') + 1
            ilosc_pamieci = form.cleaned_data['ilosc_pamieci']
            rodzaj_pamieci = form.cleaned_data['rodzaj_pamieci']
            szyna = form.cleaned_data['szyna']
            karta_graficzna = KartaGraficzna(id_karty_graficznej=id_karty_graficznej, ilosc_pamieci=ilosc_pamieci,
                                             rodzaj_pamieci=rodzaj_pamieci,
                                             szyna=szyna, id_towaru=id_towaru)
            karta_graficzna.save()

            return redirect(goods)

def goods_details(request, id_towaru):
    towar = get_object_or_404(Towary, pk=id_towaru)
    karta_graficzna = KartaGraficzna.objects.filter(id_towaru__iexact=id_towaru).first()
    pamiec = Pamiec.objects.filter(id_towaru__iexact=id_towaru).first()
    procesor = Procesor.objects.filter(id_towaru__iexact=id_towaru).first()
    plyta_glowna = PlytaGlowna.objects.filter(id_towaru__iexact=id_towaru).first()
    return render(request, 'shop/goods_details.html', {'towar':towar, 'id_towaru':id_towaru, 'karta_graficzna':karta_graficzna, 'pamiec':pamiec, 'procesor':procesor, 'plyta_glowna':plyta_glowna})

def delete_goods(request, id_towaru):
    karta_graficzna = KartaGraficzna.objects.filter(id_towaru__iexact=id_towaru).first()
    pamiec = Pamiec.objects.filter(id_towaru__iexact=id_towaru).first()
    procesor = Procesor.objects.filter(id_towaru__iexact=id_towaru).first()
    plyta_glowna = PlytaGlowna.objects.filter(id_towaru__iexact=id_towaru).first()
    if karta_graficzna:
        karta_graficzna.delete()
    elif pamiec:
        pamiec.delete()
    elif procesor:
        procesor.delete()
    elif plyta_glowna:
        plyta_glowna.delete()
    Towary.objects.filter(id_towaru__iexact=id_towaru).delete()
    return redirect(goods)

def update_goods(request, id_towaru):
    if request.method == 'POST':
        procesor = Procesor.objects.filter(id_towaru__iexact=id_towaru).first()
        if procesor:
            form = AddProcesor(request.POST)
            if form.is_valid():
                produent = form.cleaned_data['produent']
                kod_producenta = form.cleaned_data['kod_producenta']
                model = form.cleaned_data['model']
                cena = form.cleaned_data['cena']
                liczba_rdzeni = form.cleaned_data['liczba_rdzeni']
                taktowanie = form.cleaned_data['taktowanie']
                Towary.objects.filter(id_towaru__iexact=id_towaru).update(produent=produent, kod_producenta=kod_producenta,
                                                                          model=model, cena=cena)
                Procesor.objects.filter(id_towaru__iexact=id_towaru).update(liczba_rdzeni=liczba_rdzeni, taktowanie=taktowanie)

                return redirect (goods)

        pamiec = Pamiec.objects.filter(id_towaru__iexact=id_towaru).first()
        if pamiec:
            form = AddPamiec(request.POST)
            if form.is_valid():
                produent = form.cleaned_data['produent']
                kod_producenta = form.cleaned_data['kod_producenta']
                model = form.cleaned_data['model']
                cena = form.cleaned_data['cena']
                typ = form.cleaned_data['typ']
                pojemnosc = form.cleaned_data['pojemnosc']
                Towary.objects.filter(id_towaru__iexact=id_towaru).update(produent=produent,
                                                                          kod_producenta=kod_producenta,
                                                                          model=model, cena=cena)
                Pamiec.objects.filter(id_towaru__iexact=id_towaru).update(typ=typ, pojemnosc=pojemnosc)

                return redirect(goods)

        plyta_glowna = PlytaGlowna.objects.filter(id_towaru__iexact=id_towaru).first()
        if plyta_glowna:
            form = AddPlytaGlowna(request.POST)
            if form.is_valid():
                produent = form.cleaned_data['produent']
                kod_producenta = form.cleaned_data['kod_producenta']
                model = form.cleaned_data['model']
                cena = form.cleaned_data['cena']
                chipset = form.cleaned_data['chipset']
                standard_pamieci = form.cleaned_data['standard_pamieci']
                Towary.objects.filter(id_towaru__iexact=id_towaru).update(produent=produent,
                                                                          kod_producenta=kod_producenta,
                                                                          model=model, cena=cena)
                PlytaGlowna.objects.filter(id_towaru__iexact=id_towaru).update(chipset=chipset, standard_pamieci=standard_pamieci)

                return redirect(goods)

        karta_graficzna = KartaGraficzna.objects.filter(id_towaru__iexact=id_towaru).first()
        if karta_graficzna:
            form = AddKartaGraficzna(request.POST)
            if form.is_valid():
                produent = form.cleaned_data['produent']
                kod_producenta = form.cleaned_data['kod_producenta']
                model = form.cleaned_data['model']
                cena = form.cleaned_data['cena']
                ilosc_pamieci = form.cleaned_data['ilosc_pamieci']
                rodzaj_pamieci = form.cleaned_data['rodzaj_pamieci']
                szyna = form.cleaned_data['szyna']
                Towary.objects.filter(id_towaru__iexact=id_towaru).update(produent=produent,
                                                                          kod_producenta=kod_producenta,
                                                                          model=model, cena=cena)
                KartaGraficzna.objects.filter(id_towaru__iexact=id_towaru).update(ilosc_pamieci=ilosc_pamieci, rodzaj_pamieci=rodzaj_pamieci, szyna=szyna)

                return redirect(goods)