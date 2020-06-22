import os
import time
import threading

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views import View

from Photo.encryption import decrypt
from Photo.models import Photo
# Create your views here.


def validate_form(data, image):
    error = {}
    if data['caption'] == "":
        error['caption_error'] = "Caption is required"
    if data['key1'] == "":
        error['key1_error'] = "Key required to encrypt the image"
    elif len(data['key1']) < 6:
        error['key1_error'] = "Key must be greater than 6"
    if data['key1'] != data['key2']:
        error['key2_error'] = "Both key must match"
    if 'image' not in image:
        error['image_error'] = "Select the image for encryption"
    return error


class EncryptImage(View):
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        queryset = Photo.objects.all()
        page = request.GET.get('page', 1)
        photos = self.get_photos(queryset, page)
        return render(request, "index.html", {'objects': photos})

    def post(self, request, *args, **kwargs):
        default_value = {
            'caption': request.POST['caption'],
            'key1': request.POST['key1'],
        }
        error = validate_form(request.POST, request.FILES)

        if error == {}:
            photo = Photo()
            photo.caption = request.POST['caption']
            photo.image = request.FILES['image']
            photo.save(**{'key': request.POST['key1']})
            default_value = {}

        queryset = Photo.objects.all()
        page = request.GET.get('page', 1)
        photos = self.get_photos(queryset, page)
        context = dict(default_value, **dict(error, **{'objects': photos}))
        return render(request, "index.html", context)

    def get_photos(self, queryset, page):
        paginator = Paginator(queryset, self.paginate_by)
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)
        return photos


class DecryptImage(View):
    template_image = 'decryption-image.html'
    template_form = 'decryption-form.html'
    image = None

    def get(self, request, i, *args, **kwargs):
        photos = get_object_or_404(Photo, id=i)
        context = {
            'caption': photos.caption
        }
        return render(request, self.template_form, context)

    def post(self, request, i, *args, **kwargs):
        photos = get_object_or_404(Photo, id=i)
        context = {
            'caption': photos.caption
        }
        key = request.POST['key']
        if key != "":
            image = decrypt(key, photos.image.path)
            context = dict(context, **image)
            if 'error' not in image:
                self.image = context['image']
                print(self.image)
                thread = threading.Thread(target=self.thread_function, args=())
                thread.start()
                return render(request, self.template_image, context)
            else:
                return render(request, self.template_form, context)
        else:
            context['error'] = 'Key required for decryption'
            return render(request, self.template_form, context)

    def thread_function(self):
        time.sleep(10)
        os.remove(self.image)



