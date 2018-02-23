from django import forms

VIDEO_MIMETYPES = ['video/3gpp', 'video/mp4', 'video/3gpp2', 'video/webm', 'video/mpeg', 'video/mpeg', 'video/ogg', ]
IMAGE_MIMETYPES = ['image/svg+xml', 'image/webp', 'image/png', 'image/jpeg', ]
AUDIO_MIMETYPES = []  # TODO: Add support in future
VALID_MIMETYPES = VIDEO_MIMETYPES + IMAGE_MIMETYPES + AUDIO_MIMETYPES


def validate_file_extension_posts_media(value):
    if value.file.content_type not in VALID_MIMETYPES:
        raise forms.ValidationError(f'Unrecognized mimetype: {value.file.content_type}')
