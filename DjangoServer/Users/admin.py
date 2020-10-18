from django.contrib import admin

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as MyUserAdmin

from .models import Users, UsersVoiceTry, UsersFaceTry

@admin.register(Users)
class UserAdmin(MyUserAdmin):
    fieldsets = (
        (None, {'fields': ('username','email','password')}),
        #(_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active',)}),#'groups','user_permissions',
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Biometrics'), {'fields': ('face_1','face_2','voice', )}),
        (_('Iformation'), {'fields': ('age','nationality','civil_status','direction','phone','account_number','card_number','token')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'is_staff')
    search_fields = ('username', )
    ordering = ('username',)

class UsersVoiceTryAdmin(admin.ModelAdmin):
    list_display = ('user','created_dt')

admin.site.register(UsersVoiceTry, UsersVoiceTryAdmin)

class UsersFaceTryAdmin(admin.ModelAdmin):
    list_display = ('user','created_dt')

admin.site.register(UsersFaceTry, UsersFaceTryAdmin)
