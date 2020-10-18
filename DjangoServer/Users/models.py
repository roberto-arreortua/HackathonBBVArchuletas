from django.db import models
from django.contrib.auth.models import  User, AbstractBaseUser,AbstractUser, BaseUserManager, User

class Users(AbstractUser):
    
    age  = models.CharField(max_length=100, blank=True, null=True)
    nationality   = models.CharField(max_length=100, blank=True, null=True)
    civil_status  = models.CharField(max_length=100, blank=True, null=True)
    direction     = models.CharField(max_length=100, blank=True, null=True)
    phone         = models.CharField(max_length=100, blank=True, null=True) 
    account_number  = models.CharField(max_length=100, blank=True, null=True)
    card_number   = models.CharField(max_length=100, blank=True, null=True)
    face_1 = models.FileField(upload_to="Faces",  default = None, null = True, blank = True)
    face_2 = models.FileField(upload_to="Faces",  default = None, null = True, blank = True)
    voice  = models.FileField(upload_to="Voices", default = None, null = True, blank = True)
    token         = models.CharField(max_length=100, blank=True, null=True) 
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.username


class UsersVoiceTry(models.Model):
    user        = models.ForeignKey(Users,on_delete=models.SET_NULL,verbose_name="Usuario", null = True, blank=True)
    voice       = models.FileField(upload_to="VoicesTry", default = None, null = True, blank = True)
    created_dt  = models.DateTimeField(auto_now=True, verbose_name="Fecha", editable=False)

    class Meta:
        verbose_name = 'Reconocimiento de voz'
        verbose_name_plural = 'Reconocimientos de voces'
    
    def __str__(self):
        return self.user.username

class UsersFaceTry(models.Model):
    user        = models.ForeignKey(Users,on_delete=models.SET_NULL,verbose_name="Usuario", null = True, blank=True)
    face       = models.FileField(upload_to="FaceTry", default = None, null = True, blank = True)
    created_dt  = models.DateTimeField(auto_now=True, verbose_name="Fecha", editable=False)

    class Meta:
        verbose_name = 'Reconocimiento de rostro'
        verbose_name_plural = 'Reconocimientos de rostros'
    
    def __str__(self):
        return self.user.username