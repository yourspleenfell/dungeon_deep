# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import JobForm
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
        if login[1].active_char is None:
            return redirect('dungeon:create_char')
        else:
            request.session['char_id'] = login[1].active_char.id
            return redirect('/dashboard')

def create_char(request):
    user = {
        'user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'dungeon_app/create_char.html', user)

def submit_char(request):
    user = User.objects.get(id=request.session['user_id'])
    submit_char = Char.objects.char_creation(request.POST, user.id)
    if not submit_char[0]:
        for tag, error in submit_char[1].iteritems():
            messages.error(request, error, extra_tags = tag)
            return redirect('/create/character')
    request.session['char_id'] = submit_char[1].id
    return redirect('/dashboard')

def dashboard(request):
    char = Char.objects.get(id=request.session['char_id'])
    user = User.objects.get(id=request.session['user_id'])
    user_stats = {
        'user' : user,
        'char' : Char.objects.get(id = request.session['char_id']),
        'exp_percent': float(char.experience) / char.exp_to_level * 100,
    }
    return render(request, 'dungeon_app/dashboard.html', user_stats)

def submit(request):
    if request.POST['submit'] == 'Shop':
        return redirect('/shop')
    elif request.POST['submit'] == 'Play':
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': 1, 'room': 1}))
    elif request.POST['submit'] == 'Log Out':
        return redirect('/dashboard')

def shop(request):
    char = Char.objects.get(id=request.session['char_id'])
    context = {
        'char' : char,
        'consumables' : Item.objects.filter(type='consumable'),
        'weapons' : Item.objects.filter(jobs=char.job)
    }
    return render(request, 'dungeon_app/shop.html', context)

def dungeon(request, floor, room):
    char = Char.objects.get(id=request.session['char_id'])
    user = User.objects.get(id=request.session['user_id'])
    if 'img_log' not in request.session:
        request.session['img_log'] = ['']
    if 'log' not in request.session:
        request.session['log'] = []
    if 'door_open' not in request.session:
        request.session['door_open'] = False
    # if char.current_vitality <= 0:
    #     Char.objects.death(char.id, user.id)
    #     user.active_char = None
    #     user.save()
    #     del request.session['char_id']
    #     return redirect('/create/character')
    dungeon = {
        'current_floor' : floor,
        'current_room' : room,
        'rooms' : ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        'char' : char,
        'exp_percent' : float(char.experience) / char.exp_to_level * 100,
        'img_log' : request.session['img_log'],
    }
    char.current_vitality = 110
    char.save()
    return render(request, 'dungeon_app/dungeon.html', dungeon)

def random_gen(request, floor, room):
    request.session['door_open'] = True
    event_chance = random.randint(1, 20)
    if event_chance > 10:
        mon = Mon.objects.get(id=random.randint(1, 6))
        request.session['battle'] = True
        return redirect(reverse('dungeon:battle', kwargs={'floor': floor, 'room': room}))
    # elif event_chance < 10:
    #     if int(room) is 10:
    #         return redirect(reverse('dungeon:dungeon', kwargs={'floor': int(floor) + 1, 'room': 1}))
    #     else:
    #         return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': int(room) + 1}))
    elif event_chance < 10:
        request.session['treasure'] = True
        request.session['treasure_clicked'] = False
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))

def treasure(request, floor, room):
    request.session['treasure_clicked'] = True
    char = Char.objects.get(id=request.session['char_id'])
    event_chance = random.randint(1, 10)
    if event_chance > 1:
        char.gold += random.randint(1, 7) + int(floor)
        char.save()
    if int(room) is 10:
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': int(floor) + 1, 'room': 1}))
    else:
        request.session['treasure_clicked'] = False
        request.session['treasure'] = False
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': int(room) + 1}))

def battle(request, floor, room):
    char = Char.objects.get(id=request.session['char_id'])
    user = User.objects.get(id=request.session['user_id'])
    if 'vitality' not in request.session:
        mon = Mon.objects.all()
        if int(room) < 10:
            mon = Mon.objects.get(id=random.randint(1, 6))
        elif int(room) == 10:
            mon = Mon.objects.get(id=random.randint(7, 10))
        request.session['vitality'] = mon.vitality + (char.level + int(room))
        request.session['current_vitality'] = mon.vitality + (char.level + int(room))
        request.session['monster_name'] = mon.name
        request.session['attack_min'] = mon.attack_min + (char.level + 1)
        request.session['attack_max'] = mon.attack_max + (char.level + 2)
        request.session['monster_image'] = mon.image.url,
        request.session['monster_type'] = mon.type
    monster = {
        'name' : request.session['monster_name'],
        'vitality': request.session['vitality'],
        'current_vitality' : request.session['current_vitality'],
        'attack_min': request.session['attack_min'],
        'attack_max' : request.session['attack_max'],
        'type' : request.session['monster_type'],
    }
    result = Char.objects.battle(request.session['user_id'], request.session['char_id'], monster, floor, room)
    request.session['current_vitality'] = result[0]['current_vitality']
    if request.session['current_vitality'] <= 0:
        if int(room) == 10:
            floor = int(floor) + 1
            room = 1
        else:
            room = int(room) + 1
        del request.session['monster_name']
        del request.session['vitality']
        del request.session['current_vitality']
        del request.session['attack_min']
        del request.session['attack_max']
        request.session['battle'] = False
    request.session.modified = True
    return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))

def model_form_upload(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/upload')
    else:
        form = JobForm()
    return render(request, 'dungeon_app/upload.html', {
        'form' : form
    })