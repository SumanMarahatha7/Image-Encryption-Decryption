from django.db import models
from django.urls import reverse
# Create your models here.
from Photo.encryption import encrypt


class Photo(models.Model):
    caption = models.CharField(max_length=100, null=False)
    image = models.ImageField(blank=False, null=False, upload_to='Image')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, **kwargs):
        super(Photo, self).save()
        print(self.image.path, self.image.name)
        encrypt(kwargs['key'], self.image.path)
        print(kwargs)

    def get_absolute_url(self):
        return reverse('index')

    def __str__(self):
        return self.image.path
