from django import forms
from Photo.models import Photo


class PhotoForm(forms.ModelForm):
    # caption = forms.CharField(max_length=120, required=True,
    #                           widget=forms.TextInput(
    #                               attrs={
    #                                   'placeholder': 'Enter the caption',
    #                                   'class': 'border border-gray rounded',
    #                               }
    #                           ))
    # image = forms.ImageField(required=True)

    class Meta:
        model = Photo
        fields = ['caption', 'image']

