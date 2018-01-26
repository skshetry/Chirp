from PIL import Image
from django import forms
from django.core.files import File
# from testapp.models import Images
from django.contrib.auth.models import User
from .models import User_details


class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control border-input', 'placeholder': 'First Name'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class UserDetailsForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control textarea-limited border-input', 'rows': '3'}))
    gender = forms.CharField(
        max_length=2,
        widget=forms.Select(choices=User_details.GENDER_CHOICES),
    )
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker form-control'}))
    # profile_photo = forms.ImageField()

    class Meta:
        model = User_details
        fields = ('bio', 'gender', 'date_of_birth',)

# class PhotoForm(forms.ModelForm):
#     x = forms.FloatField(widget=forms.HiddenInput())
#     y = forms.FloatField(widget=forms.HiddenInput())
#     width = forms.FloatField(widget=forms.HiddenInput())
#     height = forms.FloatField(widget=forms.HiddenInput())

#     class Meta:
#         model = Photo
#         fields = ('file', 'x', 'y', 'width', 'height', )

#     def save(self):
#         photo = super(PhotoForm, self).save()

#         x = self.cleaned_data.get('x')
#         y = self.cleaned_data.get('y')
#         w = self.cleaned_data.get('width')
#         h = self.cleaned_data.get('height')

#         image = photo.open(Photo.file)
#         cropped_image = photo.crop((x, y, w+x, h+y))
#         resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
#         resized_image.save(photo.file.path)

#         return photo