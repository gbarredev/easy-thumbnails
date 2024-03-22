from django.core.files.storage import FileSystemStorage, get_storage_class
from django.utils.deconstruct import deconstructible
from django.utils.functional import LazyObject
from django.conf import settings

from easy_thumbnails.conf import settings

def get_storage():
    conf = None
    if getattr(settings, "STORAGES", None):
        if 'thumbnail' in settings.STORAGES:
            conf = settings.STORAGES['thumbnail']
        elif 'default' in settings.STORAGES:
            conf = settings.STORAGES['default']
    if not conf and getattr(settings, "THUMBNAIL_DEFAULT_STORAGE", None):
        conf = {'BACKEND': settings.THUMBNAIL_DEFAULT_STORAGE}
    if conf:
        try:
            storage_class = get_storage_class(conf['BACKEND'])
            class ThumbnailDefaultStorage(LazyObject):
                def _setup(self):
                    self._wrapped = storage_class(**conf.get('OPTIONS', {}))
            return ThumbnailDefaultStorage()
        except (ImportError, TypeError):
            from django.core.files.storage import storages
            return storages[settings.THUMBNAIL_DEFAULT_STORAGE]
    return None


@deconstructible
class ThumbnailFileSystemStorage(FileSystemStorage):
    """
    Standard file system storage.

    The default ``location`` and ``base_url`` are set to
    ``THUMBNAIL_MEDIA_ROOT`` and ``THUMBNAIL_MEDIA_URL``, falling back to the
    standard ``MEDIA_ROOT`` and ``MEDIA_URL`` if the custom settings are blank.
    """
    def __init__(self, location=None, base_url=None, *args, **kwargs):
        if location is None:
            location = settings.THUMBNAIL_MEDIA_ROOT or None
        if base_url is None:
            base_url = settings.THUMBNAIL_MEDIA_URL or None
        super().__init__(location, base_url, *args, **kwargs)


thumbnail_default_storage = get_storage()
