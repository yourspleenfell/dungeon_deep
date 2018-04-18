from __future__ import unicode_literals
from django.db import models
import random, bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PWD_REGEX = re.compile(r'(?=.*[A-Z])(?=.*[0-9])')

class UserManager(models.Manager):
    def register(self, postData):
        errors = {}
        first = postData['first_name']
        last = postData['last_name']
        username = postData['username']
        email = postData['email']
        pwd = postData['password']
        con_pwd = postData['confirm_password']
        hash_pwd = bcrypt.hashpw(pwd.encode(),bcrypt.gensalt())
        if len(first) < 3:
            errors['first_name'] = 'First name must be at least 3 characters'
        elif not first.isalpha():
            errors['first_name'] = 'First name can consist of only letters'
        if len(last) < 3:
            errors['last_name'] = 'Last name must be at least 3 characters'
        elif not last.isalpha():
            errors['last_name'] = 'Last name can consist of only letters'
        if len(username) < 6:
            errors['username_reg'] = 'Username must be at least 6 characters.'
        elif len(self.filter(username=username)) > 0:
            errors['username_reg'] = 'Username already taken'
        if len(email) is 0:
            errors['email_reg'] = 'You must enter an email address'
        elif not EMAIL_REGEX.match(email):
            errors['email_reg'] = 'Email must follow standard format'
        elif len(self.filter(email=email)) > 0:
            errors['email_reg'] = 'Email already taken' 
        if len(pwd) < 8:
            errors['password_reg'] = 'Password must be at least eight characters.'
        elif not PWD_REGEX.match(pwd):
            errors['password_reg'] = 'Password must contain one number and one capital letter'
        elif con_pwd != pwd:
            errors['password_reg'] = 'Passwords must match'
        if len(errors) > 0:
            return (False, errors)
        else:
            new_user = self.create(
                first_name = first,
                last_name = last,
                username = username,
                email = email,
                password = hash_pwd,
            )
            return (True, new_user)
    def login(self,postData):      
        user = self.filter(username = postData['username'])
        errors = {}
        if not user:
            errors['username'] = 'Username not valid.' 
        if user and not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['password'] = 'Incorrect password.'
        if len(errors) > 0:
            return (False, errors)
        else:
            return (True, self.get(username=postData['username']))

class CharManager(models.Manager):
    def char_creation(self, postData, user_id):
        errors = {}
        name = postData['name']
        job = postData['job']
        user = User.objects.get(id=user_id)
        if len(name) < 2:
            errors['char_name'] = 'Character name must be at least 2 characters'
        elif len(self.filter(name=name)) > 0:
            errors['char_name'] = 'Character name already taken'
        if len(errors) > 0:
            return (False, errors)
        if job == 'Wizard':
            new_char = self.create(
                name = name,
                job = job,
                experience = 0,
                exp_to_level = 100,
                level = 1,
                max_vitality = 50,
                current_vitality = 50,
                attack_min = 2,
                attack_max = 5,
                defense = 1,
                gold = 0,
            )
            return (True, new_char)
        elif job == 'Knight':
            new_char = self.create(
                name = name,
                job = job,
                experience = 0,
                exp_to_level = 100,
                level = 1,
                max_vitality = 100,
                current_vitality = 100,
                attack_min = 1,
                attack_max = 3,
                defense = 4,
                gold = 0,
                armor = Item.objects.get(name='None'),
                weapon = Item.objects.get(name='None'),
                active_user = user,
            )
            return (True, new_char)
        elif job == 'Archer':
            new_char = self.create(
                name = name,
                job = job,
                experience = 0,
                exp_to_level = 100,
                level = 1,
                max_vitality = 70,
                current_vitality = 70,
                attack_min = 1,
                attack_max = 4,
                defense = 2,
                gold = 0,
            )
            return (True, new_char)
        elif job == 'Monk':
            new_char = self.create(
                name = name,
                job = job,
                experience = 0,
                exp_to_level = 100,
                level = 1,
                max_vitality = 85,
                current_vitality = 85,
                attack_min = 2,
                attack_max = 3,
                defense = 3,
                gold = 0,
            )
            return (True, new_char)
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
        monster['current_vitality'] -= char_dmg
        if mon_dmg > 0:
            char.current_vitality -= mon_dmg
            char.save()
        if monster['current_vitality'] <= 0:
            char.experience += random.randint(90, 100)
            char.save()
        if char.experience >= char.exp_to_level:
            Char.objects.level_up(char.id)
        return monster

class JobManger(models.Manager):  
    def wizard(self, char_id):
        ability = random.randint(1, 20)         
        char = Char.objects.get(id=char_id)
        if ability > 15:
            dmg = random.randint(2,4)  
            dmg += char.level
            return (True, dmg)
        return (False, 0)
    def knight(self, char_id):
        ability = random.randint(1, 20) 
        char = Char.objects.get(id=char_id)
        if ability > 15:
            defense = random.randint(1,3)
            defense += char.level
            return(True, defense)
        return(False, 0)
    def archer(self, char_id):
        ability = random.randint(1, 20) 
        char = Char.objects.get(id=char_id)
        if ability > 15:
            gold = random.randint(1,10)
            char.gold += gold
            char.save()
            return(True, gold)
        return(False,0)
    def monk(self, char_id):
        ability = random.randint(1, 20) 
        char = Char.objects.get(id=char_id)
        if ability > 12:
            atk = random.randint(char.attack_min, char.attack_max)
            return(True, atk)
        return(False, 0)

class Mon(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255) # normal mon or is it a boss?
    vitality = models.IntegerField()
    attack_min = models.IntegerField()
    attack_max = models.IntegerField()
    image = models.ImageField(upload_to='monsters')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Job(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()    

class Item(models.Model):
    name = models.CharField(max_length = 255)
    cost = models.IntegerField()
    type = models.CharField(max_length=255)
    jobs = models.ManyToManyField(Job, related_name="items")
    vitality = models.IntegerField()
    defense = models.IntegerField()
    attack_max = models.IntegerField()
    attack_min = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    total_dmg_dealt = models.IntegerField(blank=True, default=0)
    total_dmg_taken = models.IntegerField(blank=True, default=0)
    monsters_killed = models.ManyToManyField(Mon, related_name="slayers", blank=True, default='')
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Char(models.Model):
    name = models.CharField(max_length=255)
    job = models.ForeignKey(Job, related_name="characters")
    experience = models.IntegerField()
    exp_to_level = models.IntegerField()
    level = models.IntegerField()
    max_vitality = models.IntegerField()
    current_vitality = models.IntegerField()
    attack_min = models.IntegerField()
    attack_max = models.IntegerField()
    defense = models.IntegerField()
    gold = models.IntegerField()
    armor = models.ForeignKey(Item, related_name="armor_wearers")
    weapon = models.ForeignKey(Item, related_name="weapon_wielders")
    inventory = models.ManyToManyField(Item, related_name="characters")
    active_user = models.ForeignKey(User, related_name="active_char")
    deaths = models.ManyToManyField(User, related_name="dead_chars")
    objects = CharManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


    