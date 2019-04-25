# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,is_active=True,is_staff=False,is_admin=False):
         if not email:
             raise ValueError("Users must have an email")
         if not password:
            raise ValueError("Users must have a Password")
         if not full_name:
             raise ValueError("Full Name is required")
         user_obj = self.model(email = self.normalize_email(email))
         user_obj.set_password(password)#Change user set_password
         user_obj.staff = is_staff
         user_obj.admin = is_admin
         user_obj.active = is_active
         user_obj.save(using=self._db)
         return user_obj

    def create_staffuser(self,email,full_name,password=None):
        user = self.create_user(email,password=password,is_staff=True)
        return user
    def create_superuser(self,email,full_name,password=None):
        user = self.create_user(email,password=password,is_staff=True,is_admin=True)
        return user

class User(AbstractBaseUser):
    email          = models.EmailField(max_length=255,unique=True,default="abc@gmail.com")
    full_name = models.CharField(max_length=255,blank=True,null=True)
    active          = models.BooleanField(default=True) #Active means can login
    staff           = models.BooleanField(default=False) #Staff user Non SuperUser
    admin           = models.BooleanField(default=False)# SuperUser
    timestamp       = models.DateTimeField(auto_now_add=True)
    #confirm        = models.BooleanField(default=False)
    #confirmed_date = models.DateTimeField(default=False)

    USERNAME_FIELD = 'email'

    #email and password required by setdefaul
    REQUIRED_FIELDS = ['full_name ']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active

class Profile(models.Model):
    user = models.OneToOneField(User)


class GuestEmail(models.Model):
    email     = models.EmailField()
    active    = models.BooleanField(default=True)
    update    = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.email
