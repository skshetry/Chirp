from b2_storage import storage
import os

class MediaStorage(storage.B2Storage):
    def __init__(self, *args, **kwargs):
        bucket_name = os.environ.get('DJANGO_BACKBLAZE_B2_MEDIA')
        super(MediaStorage, self).__init__(bucket_name=bucket_name, *args, **kwargs)

class StaticStorage(storage.B2Storage):
    pass
