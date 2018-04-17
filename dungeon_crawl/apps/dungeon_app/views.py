# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
import random

# Create your views here.
def index(request):
    if 'char_id' not in request.session:
        request.session['char_id'] = 0
    return render(request, 'dungeon_app/index.html')

def register(request):
    register = User.objects.register(request.POST)
    if not register[0]:
        for tag, error in register[1].iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    elif register[0]:
        request.session['user_id'] = register[1].id
        if not register[1].active_char:
            return redirect('dungeon:create_char')
        else:
            return redirect('/dashboard')

def login(request):
    login = User.objects.login(request.POST)
    if not login[0]:
        for tag, error in login[1].iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    elif login[0]:
        request.session['user_id'] = login[1].id
        if login[1].active_char.count() is 0:
            return redirect('dungeon:create_char')
        else:
            request.session['char_id'] = login[1].active_char.first().id
            return redirect('/dashboard')

def create_char(request):
    user = {
        'user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'dungeon_app/create_char.html', user)

def submit_char(request):
    submit_char = Char.objects.char_creation(request.POST, request.session['user_id'])
    if not submit_char[0]:
        for tag, error in submit_char[1].iteritems():
            messages.error(request, error, extra_tags = tag)
            return redirect('/create/character')
    request.session['char_id'] = submit_char[1].id
    return redirect('/dashboard')

def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    char = Char.objects.get(id = request.session['char_id'])
    user_stats = {
        'user' : user,
        'monsters_killed': user.monsters_killed.filter(type='normal').count(),
        'bosses_killed': user.monsters_killed.filter(type='boss').count(),
        'character' : Char.objects.get(id = request.session['char_id']),
        'exp_percent': float(char.experience) / char.exp_to_level * 100
    }
    return render(request, 'dungeon_app/dashboard.html', user_stats)

def submit(request):
    if request.POST['submit'] == 'Shop':
        print request.POST['submit']
        return redirect('/dashboard')
    elif request.POST['submit'] == 'Play':
        print request.POST['submit']
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': 1, 'room': 1}))
    elif request.POST['submit'] == 'Log Out':
        print request.POST['submit']
        return redirect('/dashboard')

def dungeon(request, floor, room):
    char = Char.objects.get(id=request.session['char_id'])
    user = User.objects.get(id=request.session['user_id'])
    if 'log' not in request.session:
        request.session['log'] = {}
    dungeon = {
        'current_floor' : floor,
        'current_room' : room,
        'character' : char,
        'exp_percent' : float(char.experience) / char.exp_to_level * 100,
    }
    return render(request, 'dungeon_app/dungeon.html', dungeon)

def battle(request, floor, room):
    char = Char.objects.get(id=request.session['char_id'])
    user = User.objects.get(id=request.session['user_id'])
    if 'vitality' not in request.session:
        mon = Mon.objects.get(id=random.randint(1, 1))
        request.session['vitality'] = mon.vitality + char.level
        request.session['current_vitality'] = mon.vitality + char.level
        request.session['monster_name'] = mon.name
        request.session['attack_min'] = mon.attack_min + char.level
        request.session['attack_max'] = mon.attack_max + char.level
    monster = {
        'name' : request.session['monster_name'],
        'vitality': request.session['vitality'],
        'current_vitality' : request.session['current_vitality'],
        'attack_min': request.session['attack_min'],
        'attack_max' : request.session['attack_max']
    }
    enemy = Char.objects.battle(request.session['char_id'], monster)
    request.session['current_vitality'] = enemy['current_vitality']
    if request.session['current_vitality'] <= 0:
        monster = Mon.objects.filter(name=request.session['monster_name']).first()
        user.monsters_killed.add(monster)
        user.save()
        del request.session['monster_name']
        del request.session['vitality']
        del request.session['current_vitality']
        del request.session['attack_min']
        del request.session['attack_max']
    # del request.session['attack_min']
    # del request.session['attack_max']
    # del request.session['vitality']
    # del request.session['name']
    print request.session['mon_image']
    request.session.modified = True
    return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))