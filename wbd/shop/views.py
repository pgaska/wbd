from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect

from .models import Hurtownie, Poczta, Magazyny

# Create your views here.
def index(request):
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
    magazyny = Magazyny.objects.all()
    return render(request, 'shop/magazines.html', {'magazyny':magazyny})

def workers(request):
    pass

def goods(request):
    pass