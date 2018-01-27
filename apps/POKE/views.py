# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from ..log_reg.models import User
from .models import *
from django.db.models import Count


def index(request):
    if 'user_name' not in request.session:
        messages.add_message(request, messages.INFO, "you should be logged in first to view this page")
        return redirect('/')
    id = request.session['user_id']
    kedir_in = User.objects.get(id = request.session['user_id'])
    others = User.objects.all().exclude(id = request.session['user_id'])
    kedirs_pokes = Poke.objects.kedirs_pokes(id)
    pokers = Poke.objects.who_poked_kedir(id)
    pok = []
    for each in pokers:
        pok.append(User.objects.get(alias = each['poker__alias']))
    dhuma = []

    for each in pok:
        qabiye = {}
        count = Poke.objects.filter(poker = each, poked = kedir_in).count()
        qabiye['name'] = each.alias
        qabiye['count'] = count
        dhuma.append(qabiye)

    context = {
        'others':others,
        'kedirs_pokes':kedirs_pokes,
        'pokers':dhuma
    }
    return render(request, "POKE/index.html", context)       

def logout(request):
    request.session.flush()
    return redirect('/main')

def poke(request):
    if request.method == 'POST':
        Poke.objects.poke(request.POST)
        return redirect('/pokes/') 