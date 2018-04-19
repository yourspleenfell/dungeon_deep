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
        print user.id
        if len(name) < 2:
            errors['char_name'] = 'Character name must be at least 2 characters'
        elif len(self.filter(name=name)) > 0:
            errors['char_name'] = 'Character name already taken'
        if len(errors) > 0:
            return (False, errors)
        if job == 'Wizard':
            new_char = self.create(
                name = name,
                job = Job.objects.get(name=job),
                experience = 0,
                exp_to_level = 100,
                level = 1,
                max_vitality = 50,
                current_vitality = 50,
                attack_min = 2,
                attack_max = 5,
                defense = 1,
                gold = 0,
                armor = Item.objects.get(name='None'),
                weapon = Item.objects.get(name='None'),
            )
            user.active_char = new_char
            user.save()
            return (True, new_char)
        elif job == 'Knight':
            new_char = self.create(
                name = name,
                job = Job.objects.get(name=job),
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
            )
            user.active_char = new_char
            user.save()
            return (True, new_char)
        elif job == 'Archer':
            new_char = self.create(
                name = name,
                job = Job.objects.get(name=job),
                experience = 0,
                exp_to_level = 100,
                level = 1,
                max_vitality = 70,
                current_vitality = 70,
                attack_min = 1,
                attack_max = 4,
                defense = 2,
                gold = 0,
                armor = Item.objects.get(name='None'),
                weapon = Item.objects.get(name='None'),
            )
            user.active_char = new_char
            user.save()
            return (True, new_char)
        elif job == 'Monk':
            new_char = self.create(
                name = name,
                job = Job.objects.get(name=job),
                experience = 0,
                exp_to_level = 100,
                level = 1,
                max_vitality = 85,
                current_vitality = 85,
                attack_min = 2,
                attack_max = 3,
                defense = 3,
                gold = 0,
                armor = Item.objects.get(name='None'),
                weapon = Item.objects.get(name='None'),
            )
            user.active_char = new_char
            user.save()
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
    def battle(self, user_id, char_id, monster, floor, room):
        user = User.objects.get(id=user_id)
        char = self.get(id=char_id)
        char_dmg = (False, 0)
        char_hit_chance = random.randint(1, 30)
        mon_dmg = (False, 0)
        if char_hit_chance is 1:
            char_dmg = (False, 0)
        else:
            char_dmg = (True, random.randint(char.attack_min, char.attack_max))
            user.total_dmg_dealt += char_dmg[1]
        if monster['type'] == 'normal':
            mon_hit_chance = random.randint(1, 15)
            if mon_hit_chance is 1:
                mon_dmg = (False, 0)
            else:
                mon_dmg = (True, (random.randint(monster['attack_min'], monster['attack_max']) - char.defense))
                monster['current_vitality'] -= char_dmg[1]
                if mon_dmg > 0:
                    char.current_vitality -= mon_dmg[1]
                    char.save()
                    user.total_dmg_taken += mon_dmg[1]
                    user.save()
                if monster['current_vitality'] <= 0:
                    char.experience += random.randint(10, 20)
                    char.num_monsters_killed += 1
                    char.monsters_killed += monster['name'] + ', '
                    user.total_monsters_killed += 1
                    char.save()
                    user.save()
                if char.experience >= char.exp_to_level:
                    Char.objects.level_up(char.id)
        elif monster['type'] == 'boss':
            mon_hit_chance = random.randint(1, 15)
            if mon_hit_chance is 1:
                mon_dmg = (False, 0)
            else:
                mon_dmg = (True, (random.randint(monster['attack_min'], monster['attack_max']) - char.defense))
                monster['current_vitality'] -= char_dmg[1]
                if mon_dmg > 0:
                    char.current_vitality -= mon_dmg[1]
                    char.save()
                    user.total_dmg_taken += mon_dmg[1]
                    user.save()
                if monster['current_vitality'] <= 0:
                    char.experience += random.randint(100, 200)
                    char.num_monsters_killed += 1
                    char.monsters_killed += monster['name'] + ', '
                    user.total_bosses_killed += 1
                    char.save()
                    user.save()
                if char.experience >= char.exp_to_level:
                    Char.objects.level_up(char.id)
        return (monster, mon_dmg, char_dmg)
    def death(self, char_id, user_id):
        user = User.objects.get(id=user_id)
        char = Char.objects.get(id=char_id)
        user.characters.add(char)
        return user

class JobManager(models.Manager):
    def ability(self, char_id):
        char = Char.objects.get(id=char_id)
        if char.job == 'Archer':
            print "hello"

class Job(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField()
    objects = JobManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Mon(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    vitality = models.IntegerField()
    attack_min = models.IntegerField()
    attack_max = models.IntegerField()
    image = models.ImageField(upload_to='monsters')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Item(models.Model):
    name = models.CharField(max_length = 255)
    cost = models.IntegerField()
    type = models.CharField(max_length=255)
    jobs = models.ManyToManyField(Job, related_name="items")
    vitality = models.IntegerField()
    defense = models.IntegerField()
    attack_max = models.IntegerField()
    attack_min = models.IntegerField()
    image = models.ImageField(upload_to='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    num_monsters_killed = models.IntegerField(default=0)
    monsters_killed = models.TextField(blank=True, null=True)
    objects = CharManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    active_char = models.ForeignKey(Char, related_name="active_user", null=True)
    characters = models.ManyToManyField(Char, related_name="created_by")
    total_dmg_dealt = models.IntegerField(default=0)
    total_dmg_taken = models.IntegerField(default=0)
    total_monsters_killed = models.IntegerField(default=0)
    total_bosses_killed = models.IntegerField(default=0)
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)