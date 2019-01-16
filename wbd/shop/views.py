from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Max


from .models import Hurtownie, Poczta, Magazyny
from .forms import AddMagazine

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

def workers(request):
    pass

def goods(request):
    pass