from __future__ import unicode_literals
from django.db import models
import random, bcrypt

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 3:
            errors['first_name'] = 'First name must be at least 3 characters'
        if len(postData['Last_name']) < 3:
            errors['last_name'] = 'Last name must be at least 3 characters'
        if len(postData['username']) < 6:
            errors['username'] = 'Username must be at least 6 characters.'  
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least eight characters.'  
        if postData['confirm_password'] != postData['password']:
            errors['confirm_password'] = 'Passwords must match'
        
        return errors

    def login(self,postData):
        
        user = User.objects.filter(username = postData['username'])
        errors = {}
        if not user:
            errors['username'] = 'Username not valid.' 
        if user and not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['password'] = 'Incorrect password.'
        return errors

class CharManager(models.Manager):
    def char_creation(self, postData):
        print postData['job']
        if postData['job'] == 'Wizard':
            new_char = self.create(
                name = postData['name'],
                job = postData['job'],
                experience = 0,
                exp_to_level = 100,
                level = 1,
                vitality = 50,
                attack_min = 2,
                attack_max = 5,
                defense = 1,
                gold = 0,
            )
            return new_char
        elif postData['job'] == 'Knight':
            new_char = self.create(
                name = postData['name'],
                job = postData['job'],
                experience = 0,
                exp_to_level = 100,
                level = 1,
                vitality = 100,
                attack_min = 1,
                attack_max = 3,
                defense = 4,
                gold = 0,
            )
            return new_char
        elif postData['job'] == 'Archer':
            new_char = self.create(
                name = postData['name'],
                job = postData['job'],
                experience = 0,
                exp_to_level = 100,
                level = 1,
                vitality = 70,
                attack_min = 1,
                attack_max = 4,
                defense = 2,
                gold = 0,
            )
            return new_char
        elif postData['job'] == 'Monk':
            new_char = self.create(
                name = postData['name'],
                job = postData['job'],
                experience = 0,
                exp_to_level = 100,
                level = 1,
                vitality = 85,
                attack_min = 2,
                attack_max = 3,
                defense = 3,
                gold = 0,
            )
            return new_char
    def level_up(self, id):
        char = self.get(id=id)
        char.level += 1
        exp_remaining = char.experience - char.exp_to_level
        char.exp_to_level = char.exp_to_level * 2
        char.experience = exp_remaining
        char.max_vitality += 10
        char.current_vitality = char.max_vitality
        char.attack_min += 1
        char.attack_max += 1
        char.defense += 1
        char.save()
    def battle(self, char_id, monster):
        char = self.get(id=char_id)
        char_dmg = random.randint(char.attack_min, char.attack_max)
        mon_dmg = (random.randint(monster['attack_min'], monster['attack_max']) - char.defense)
        monster['vitality'] -= char_dmg
        if mon_dmg > 0:
            char.current_vitality -= mon_dmg
            char.save()
        if monster['vitality'] <= 0:
            char.experience += random.randint(90, 100)
            # char.monsters_killed.add(monster)
            char.save()
        if char.experience >= char.exp_to_level:
            Char.objects.level_up(char.id)
        return monster

class Mon(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255) # normal mon or is it a boss?
    vitality = models.IntegerField()
    attack_min = models.IntegerField()
    attack_max = models.IntegerField()
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
    name = models.CharField(max_length=255)
    job = models.CharField(max_length=255)
    experience = models.IntegerField()
    exp_to_level = models.IntegerField()
    level = models.IntegerField()
    max_vitality = models.IntegerField()
    current_vitality = models.IntegerField()
    attack_min = models.IntegerField()
    attack_max = models.IntegerField()
    defense = models.IntegerField()
    gold = models.IntegerField()
    inventory = models.ManyToManyField(Item, related_name="characters")
    objects = CharManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    active_char = models.ForeignKey(Char, related_name="active_user")
    dead_chars = models.ManyToManyField(Char, related_name="dead_user")
    total_dmg_dealt = models.IntegerField()
    total_dmg_taken = models.IntegerField()
    monsters_killed = models.ManyToManyField(Mon, related_name="slayers")
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)