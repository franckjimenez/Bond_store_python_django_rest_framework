from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('The user must have a valid email.')
        email=self.normalize_email(email)
        if not username:
            raise ValueError('The user must have a valid username.')
        user=self.model(email=email,username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user=self.create_user(email,username,password)
        
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    id=models.AutoField(primary_key=True)
    username= models.CharField(unique=True, max_length=100)
    email=models.EmailField(max_length=255,unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

    class Meta:
        verbose_name='User'
        verbose_name_plural="Users"
        ordering=['id']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm,obj=None):
        return True
    def has_module_perms(self, app_label):
        return True

    def get_short_name(self):
        return self.email
    
    def get_full_name(self):
        return self.username
        
    
