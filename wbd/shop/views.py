from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Hurtownie, Poczta

# Create your views here.
def index(request):
    return render(request, 'shop/index.html')

def hurtownia(request, hurtownia_id=1):
    hurtownia = get_object_or_404(Hurtownie, pk=hurtownia_id)
    return render(request, 'shop/hurtownia.html', {'hurtownia': hurtownia})