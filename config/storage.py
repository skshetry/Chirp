from b2_storage import storage
from django.conf import settings


class MediaStorage(storage.B2Storage):
    def __init__(self, *args, **kwargs):
        super(MediaStorage, self).__init__(
            bucket_name=settings.BACKBLAZEB2_BUCKET_NAME_MEDIA,
            *args, **kwargs)


class StaticStorage(storage.B2Storage):
    pass
