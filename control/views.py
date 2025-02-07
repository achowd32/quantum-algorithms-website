from django.shortcuts import render
from django.http import HttpResponse
from control.algorithms.essentials import *
from control.algorithms.rng import randomNumber
from control.algorithms.qft import applyQFT
from control.algorithms.grover import groverCirc
from control.algorithms.shor import shor15
from .forms import QftForm, ShorForm

def home(request):
    return render(request, "home.html")

def rng(request):
    randNum = randomNumber(0, 5, 6)
    context = {'randNum': randNum}
    return render(request, "rng.html", context)

def qft(request):
    if request.method == 'POST':
        form = QftForm(request.POST)
        if form.is_valid():
            state = form.cleaned_data['state']
            try:
                qft_state = list(applyQFT(state))
            except:
                return render(request, "qft.html", {"error": True}) #insert "form": form if needed
            else:
                return render(request, "qft.html", {"state": qft_state})
        else:
            return render(request, "qft.html")
    else:
        return render(request, "qft.html")

def shor(request):
    if request.method == 'POST':
        form = ShorForm(request.POST)
        if form.is_valid():
            a_val = form.cleaned_data['a_val']
            try:
                result = shor15(a_val)
            except:
                r_val = result[0]
                factors = result[1]
                qpe_bool = result[2]
                return render(request, "shor.html", {"display": True, "error": True})
            else:
                r_val = result[0]
                factors = result[1]
                qpe_bool = result[2]
                return render(request, "shor.html", {"display": True, "r_val": r_val, "factors": factors, "qpe_bool": qpe_bool})
        else:
            return render(request, "shor.html", {"display": False})
    else:
        return render(request, "shor.html", {"display": False})

def grover(request):
    result = sample(groverCirc())
    validity = 'valid!'
    sum_one = int(result[0]) + int(result[1]) + int(result[2])
    sum_two = int(result[3]) + int(result[4]) + int(result[5])
    if sum_one != sum_two:
        validity = 'invalid'
    context = {'string_one': result[:3], 'string_two': result[3:], 'validity': validity}
    return render(request, "grover.html", context)