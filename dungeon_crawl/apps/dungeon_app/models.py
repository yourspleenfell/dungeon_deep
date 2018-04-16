from __future__ import unicode_literals
from django.db import models

class UserManager(models.Manager):
    print "hello"

class CharManager(models.Manager):
    print "hello"

class MonMan(models.Manager):
    print "hello"

class Mon(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255) #normal mon or is it a boss?
    job = models.CharField(max_length=255) #is this a goblin? skeleton?
    level = models.IntegerField()
    vitality = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Item(models.Model):
    gold = models.IntegerField()
    weapon = models.CharField(max_length=255)
    armor = models.CharField(max_length=255)
    potion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Char(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    experience = models.IntegerField()
    level = models.IntegerField()
    vitality = models.IntegerField()
    attack = models.IntegerField()
    defense = models.IntegerField()
    inventory = models.ManyToManyField(Item, related_name="characters")
    objects = CharManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    active_char = models.ForeignKey(Char, related_name="active_user")
    dead_chars = models.ManyToManyField(Char, related_name="dead_user")
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)