from PIL import Image
from django import forms
from django.core.files import File
from django.contrib.auth.models import User
from .models import User_details


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


class ProfilePhotoForm(forms.ModelForm):
    profile_x = forms.FloatField(widget=forms.HiddenInput())
    profile_y = forms.FloatField(widget=forms.HiddenInput())
    profile_width = forms.FloatField(widget=forms.HiddenInput())
    profile_height = forms.FloatField(widget=forms.HiddenInput())
    DIMENSIONS = (200, 200)
    class Meta:
            model = User_details
            fields = ('profile_photo', 'profile_x', 'profile_y', 'profile_height', 'profile_width')

    def save(self):
        photo = super(ProfilePhotoForm, self).save()
        x = self.cleaned_data.get('profile_x')
        y = self.cleaned_data.get('profile_y')
        w = self.cleaned_data.get('profile_width')
        h = self.cleaned_data.get('profile_height')

        image = Image.open(photo.profile_photo)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize(self.DIMENSIONS, Image.ANTIALIAS)
        resized_image.save(photo.profile_photo.name)

        return photo


class CoverPhotoForm(forms.ModelForm):
    cover_x = forms.FloatField(widget=forms.HiddenInput())
    cover_y = forms.FloatField(widget=forms.HiddenInput())
    cover_width = forms.FloatField(widget=forms.HiddenInput())
    cover_height = forms.FloatField(widget=forms.HiddenInput())
    DIMENSIONS = (1357, 334)
    class Meta:
            model = User_details
            fields = ('cover_photo', 'cover_x', 'cover_y', 'cover_height', 'cover_width')

    def save(self):
        photo = super(CoverPhotoForm, self).save()
        x = self.cleaned_data.get('cover_x')
        y = self.cleaned_data.get('cover_y')
        w = self.cleaned_data.get('cover_width')
        h = self.cleaned_data.get('cover_height')

        image = Image.open(photo.cover_photo)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize(self.DIMENSIONS, Image.ANTIALIAS)
        resized_image.save(photo.cover_photo.name)

        return photo