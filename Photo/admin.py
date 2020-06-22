from django.contrib import admin
from Photo.models import Photo
# Register your models here.


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'image')


admin.site.register(Photo, PhotoAdmin)
