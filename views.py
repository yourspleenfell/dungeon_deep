# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
import random
from django.contrib import messages

# Create your views here.
def index(request):
    for objects in User.objects.all():
        context = {
            "first_name":objects.first_name,
            "last_name":objects.last_name,
            "username":objects.username,
            "password":objects.password,
            "created_at":objects.created_at,
            "updated_at":objects.updated_at,
            "user_data":objects.all()
        }
        
    if 'char_id' not in request.session:
        request.session['char_id'] = 0
    return render(request, 'dungeon_app/index.html', context)

def register(request):
    errors = User.objects.validator(request.POST)
    hashedpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')    
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username=request.POST['username'], password=hashedpw)
    request.session['logged_in'] = user.id
    return redirect('/dashboard') 

def dashboard(request):
    if User.objects.get(id=request.session['logged_in']) == User.objects.last():
        status = "registered!"
    else:
        status = "logged in!"
    return render(request, '/dashboard')

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