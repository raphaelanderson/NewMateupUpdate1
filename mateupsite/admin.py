from django.contrib import admin
from .models import Attribute, Profile

# Register your models here.
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ('attributes',)
