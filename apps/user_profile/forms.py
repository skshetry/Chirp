from PIL import Image
from django import forms
from django.core.files import File
from django.contrib.auth.models import User
from .models import User_details
from django.core.files.storage import default_storage as storage
from datetime import date

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border-input', 'placeholder': 'First Name'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserDetailsForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control textarea-limited border-input', 'rows': '3', 'maxlength': '140'}), required=False)
    gender = forms.CharField(
        max_length=2,
        widget=forms.Select(choices=User_details.GENDER_CHOICES),
        required=False
    )
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'datetimepicker form-control'}), required=False)
    class Meta:
        model = User_details
        fields = ('bio', 'gender', 'date_of_birth')
    
    def clean_image(self, photo_name):
        image_file = photo_name
        if not image_file.name.endswith('.jpg'):
            raise forms.ValidationError("Only .jpg image accepted")
        return image_file

    def clean_date(self):
        birth_date = self.cleaned_data['date_of_birth']
        if birth_date > date.today():
            raise forms.ValidationError("The date cannot be in the Future.")


class ProfilePhotoForm(forms.ModelForm):
    profile_x = forms.FloatField(widget=forms.HiddenInput())
    profile_y = forms.FloatField(widget=forms.HiddenInput())
    profile_width = forms.FloatField(widget=forms.HiddenInput())
    profile_height = forms.FloatField(widget=forms.HiddenInput())
    DIMENSIONS = (200, 200)
    photo_name = 'profile_photo'

    class Meta:
            model = User_details
            fields = ('profile_photo', 'profile_x', 'profile_y', 'profile_height', 'profile_width')
            widgets = {
                'profile_photo': forms.FileInput(attrs={'accept': 'image/jpeg'})
            }

    def save(self):
        photo = super(ProfilePhotoForm, self).save()
        x = self.cleaned_data.get('profile_x')
        y = self.cleaned_data.get('profile_y')
        w = self.cleaned_data.get('profile_width')
        h = self.cleaned_data.get('profile_height')

        clean_image_file = UserDetailsForm.clean_image(self, photo.profile_photo)
        image = Image.open(clean_image_file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize(self.DIMENSIONS, Image.ANTIALIAS)
        resized_image.format = image.format
        resized_image.name = photo.profile_photo.name
        fh = storage.open(resized_image.name, "w")
        format = resized_image.format
        resized_image.save(fh, format)
        fh.close()

        return resized_image


class CoverPhotoForm(forms.ModelForm):
    cover_x = forms.FloatField(widget=forms.HiddenInput())
    cover_y = forms.FloatField(widget=forms.HiddenInput())
    cover_width = forms.FloatField(widget=forms.HiddenInput())
    cover_height = forms.FloatField(widget=forms.HiddenInput())
    DIMENSIONS = (1357, 334)
    photo_name = 'cover_photo'

    class Meta:
            model = User_details
            fields = ('cover_photo', 'cover_x', 'cover_y', 'cover_height', 'cover_width')
            widgets = {
                'cover_photo': forms.FileInput(attrs={'accept': 'image/jpeg'})
            }

    def save(self):
        photo = super(CoverPhotoForm, self).save()
        x = self.cleaned_data.get('cover_x')
        y = self.cleaned_data.get('cover_y')
        w = self.cleaned_data.get('cover_width')
        h = self.cleaned_data.get('cover_height')

        clean_image_file = UserDetailsForm.clean_image(self, photo.cover_photo)
        image = Image.open(clean_image_file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize(self.DIMENSIONS, Image.ANTIALIAS)
        resized_image.format = image.format
        resized_image.name = photo.cover_photo.name
        fh = storage.open(resized_image.name, "w")
        format = resized_image.format
        resized_image.save(fh, format)
        fh.close()

        return resized_image