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
    if request.method == 'POST':
        char = Char.objects.get(id=request.session['char_id'])
        item = Item.objects.get(id=request.POST['item'])
        char.gold -= item.cost
        char.inventory.add(item)
        if item.type != 'consumable':
            Item.objects.equip(char.id, item.id)
        return redirect('/shop')
    else:
        char = Char.objects.get(id=request.session['char_id'])
        context = {
            'char' : char,
            'consumables' : Item.objects.filter(type='consumable'),
            'weapons' : Item.objects.filter(jobs=char.job).filter(type='weapon'),
            'armor' : Item.objects.filter(jobs=char.job).filter(type='armor'),
        }
        return render(request, 'dungeon_app/shop.html', context)

def dungeon(request, floor, room):        
    char = Char.objects.get(id=request.session['char_id'])
    if 'engaged' not in request.session:
        request.session['engaged'] = False   
    if 'event' not in request.session:
        request.session['event'] = (False, False)
    if 'log' not in request.session:
        request.session['log'] = []
    dungeon = {
        'current_floor' : floor,
        'current_room' : room,
        'rooms' : ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
        'char' : char,
        'inventory' : Item.objects.filter(type='consumable')[:3],
        'exp_percent' : float(char.experience) / char.exp_to_level * 100,
        'event' : Item.objects.get(id=1),
    }
    # if char.current_vitality <= 0:
    #     Char.objects.death(char.id, user.id)
    #     user.active_char = None
    #     user.save()
    #     del request.session['char_id']
    #     return redirect('/create/character')
    if request.session['event'][0]:
        mon = Mon.objects.get(id = request.session['event'][2])
        dungeon['event'] = mon
        char.current_vitality = 110
        char.save()
        return render(request, 'dungeon_app/dungeon.html', dungeon)
    elif request.session['event'][1]:
        char.current_vitality = 110
        char.save()
        return render(request, 'dungeon_app/dungeon.html', dungeon)
    else:
        char.current_vitality = 110
        char.save()
        return render(request, 'dungeon_app/dungeon.html', dungeon)

def random_gen(request, floor, room):
    request.session['door_open'] = True
    chance = random.randint(1, 3)
    if int(room) is 10:
        mon = Mon.objects.get(id = random.randint(7, 10))
        new_mon = Mon.objects.create(
            name = mon.name,
            type = mon.type,
            vitality = mon.vitality + int(room),
            current_vitality = mon.vitality + int(room),
            attack_min = mon.attack_min + int(floor),
            attack_max = mon.attack_min + int(floor),
            image = mon.image,
            image_dead = mon.image_dead,
        )
        request.session['event'] = (True, False, new_mon.id)
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))
    if chance > 3:
        mon = Mon.objects.get(id = random.randint(1, 6))
        new_mon = Mon.objects.create(
            name = mon.name,
            type = mon.type,
            vitality = mon.vitality + int(room),
            current_vitality = mon.vitality + int(room),
            attack_min = mon.attack_min + int(floor),
            attack_max = mon.attack_min + int(floor),
            image = mon.image,
            image_dead = mon.image_dead,
        )
        request.session['event'] = (True, False, new_mon.id)
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))
    # elif chance < 10:
    #     if int(room) is 10:
    #         return redirect(reverse('dungeon:dungeon', kwargs={'floor': int(floor) + 1, 'room': 1}))
    #     else:
    #         return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': int(room) + 1}))
    elif chance < 4:
        request.session['event'] = (False, True, 0)
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))

def progress(request, floor, room):
    request.session['event'] = (False, False, 0)
    request.session['engaged'] = False
    if int(room) is 10:
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': int(floor) + 1, 'room': 1}))
    else:
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': int(room) + 1}))

def treasure(request, floor, room):
    request.session['engaged'] = True
    chance = random.randint(1, 20) + int(floor)
    treasure = Item.objects.treasure(request.session['char_id'], floor, chance)
    print treasure
    return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))

def battle(request, floor, room):
    mon_id = request.session['event'][2]
    mon = Mon.objects.get(id=mon_id)
    if not request.session['engaged']:
        request.session['engaged'] = True
        battle = Char.objects.battle(request.session['user_id'], request.session['char_id'], mon, floor, room)
        request.session['event'][2] = battle[0].id
        return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))
    else:
        battle = Char.objects.battle(request.session['user_id'], request.session['char_id'], mon, floor, room)
        if battle[0].current_vitality <= 0:
            battle[0].current_vitality = 0
            battle[0].save()
            return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))
        else:
            return redirect(reverse('dungeon:dungeon', kwargs={'floor': floor, 'room': room}))   

def model_form_upload(request):
    if request.method == 'POST':
        mon = Mon.objects.get(id=request.POST['mon_id'])
        mon.image_dead = request.FILES['image']
        mon.save()
        return redirect('/upload')
    else:
        context = {
            'mobs' : Mon.objects.all()[:10],
        }
        return render(request, 'dungeon_app/upload.html', context)