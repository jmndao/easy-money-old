# Original authors: Andres Torres and Maximiliano Cecilia

import os.path
import itertools
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
from dropbox import Dropbox
from dropbox.exceptions import ApiError
from dropbox.files import FolderMetadata, FileMetadata, DeleteError
from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from .settings import ACCESS_TOKEN, ROOT_FOLDER, DEFAULT_ROOT_FOLDER


@deconstructible
class DropboxStorage(Storage):
    """
    A storage class providing access to resources in a Dropbox folder.
    """

    def __init__(self, token=ACCESS_TOKEN, location=ROOT_FOLDER):
        if not token:
            raise ImproperlyConfigured("You must configure an access token at "
                                       "'settings.DROPBOX_ACCESS_TOKEN'.")

        self.client = Dropbox(token)
        self.account_info = self.client.users_get_current_account()
        self.location = location or DEFAULT_ROOT_FOLDER
        self.base_url = 'https://dl.dropboxusercontent.com/'

    def _get_abs_path(self, name):
        return os.path.realpath(os.path.join(self.location, name))

    def _open(self, name, mode='rb'):
        name = self._get_abs_path(name)
        remote_file = DropboxFile(name, self, mode=mode)
        return remote_file

    def _save(self, name, content):
        name = self._get_abs_path(name)
        directory = os.path.dirname(name)
        if not self.exists(directory) and directory:
            self.client.files_create_folder(directory)
        # response = self.client.files_get_metadata(directory)
        # if not response['is_dir']:
        #     raise IOError("%s exists and is not a directory." % directory)
        abs_name = os.path.realpath(os.path.join(self.location, name))
        self.client.files_upload(content.read(), abs_name)
        return name

    def delete(self, name):
        name = self._get_abs_path(name)
        try:
            self.client.files_delete(name)
        except ApiError as e:
            if isinstance(e.error, DeleteError)\
                    and e.error.is_path_lookup()\
                    and e.error.get_path_lookup().is_not_found():
                # not found
                return False
            # error
            raise e
        # deleted
        return True

    def exists(self, name):
        name = self._get_abs_path(name)
        try:
            self.client.files_get_metadata(name)
        except ApiError as e:
            if hasattr(e.error, 'is_path')\
                    and e.error.is_path()\
                    and e.error.get_path().is_not_found():
                # not found
                return False
            # error
            raise e
        # found
        return True

    def listdir(self, path):
        path = self._get_abs_path(path)
        response = self.client.files_list_folder(path)
        directories = []
        files = []
        for entry in response.entries:
            if isinstance(entry, FolderMetadata):
                directories.append(os.path.basename(entry.path_display))
            elif isinstance(entry, FileMetadata):
                files.append(os.path.basename(entry.path_display))
        return directories, files

    def size(self, name):
        name = self._get_abs_path(name)
        return self.client.files_get_metadata(name).size

    def url(self, name):
        name = self._get_abs_path(name)
        return self.client.files_get_temporary_link(name).link

    def modified_time(self, name):
        name = self._get_abs_path(name)
        return self.client.files_get_metadata(name).server_modified

    def accessed_time(self, name):
        name = self._get_abs_path(name)
        # Note to the unwary, this is actually an mtime
        return self.client.files_get_metadata(name).client_modified

    def get_available_name(self, name, max_length=None):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        name = self._get_abs_path(name)
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        # If the filename already exists, add an underscore and a number (before
        # the file extension, if one exists) to the filename until the generated
        # filename doesn't exist.
        count = itertools.count(1)
        while self.exists(name):
            # file_ext includes the dot.
            _fn = "%s_%s%s" % (file_root, next(count), file_ext)
            name = os.path.join(dir_name, _fn)

        return name


class DropboxFile(File):
    def __init__(self, name, storage, mode):
        self._storage = storage
        self._mode = mode
        self._is_dirty = False
        self.file = StringIO()
        self.start_range = 0
        self._name = name

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self, num_bytes=None):
        metadata, response = self._storage.client.files_download(self._name)
        return response.content

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was opened for read-only access.")
        self.file = StringIO(content)
        self._is_dirty = True

    def close(self):
        if self._is_dirty:
            self._storage.client.files_upload(self.file.getvalue(), self._name)
        self.file.close()
