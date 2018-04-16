# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
import random

# Create your views here.
def index(request):
    if 'char_id' not in request.session:
        request.session['char_id'] = 0
    return render(request, 'dungeon_app/index.html')

def create_char(request):
    new_char = Char.objects.char_creation(request.POST)
    request.session['char_id'] = new_char.id
    return redirect('/')

def battle(request):
    char = Char.objects.get(id=request.session['char_id'])
    if 'vitality' not in request.session:
        mon = Mon.objects.get(id=random.randint(1, 1))
        request.session['vitality'] = mon.vitality + char.level
        request.session['name'] = mon.name
        request.session['attack_min'] = mon.attack_min + char.level
        request.session['attack_max'] = mon.attack_max + char.level
    monster = {
        'name' : request.session['name'],
        'vitality' : request.session['vitality'],
        'attack_min': request.session['attack_min'],
        'attack_max' : request.session['attack_max']
    }
    enemy = Char.objects.battle(request.session['char_id'], monster)
    request.session['vitality'] = enemy['vitality']
    if request.session['vitality'] <= 0:
        del request.session['name']
        del request.session['vitality']
        del request.session['attack_min']
        del request.session['attack_max']
    # del request.session['attack_min']
    # del request.session['attack_max']
    # del request.session['vitality']
    # del request.session['name']
    request.session.modified = True
    print char.current_vitality
    return redirect('/')