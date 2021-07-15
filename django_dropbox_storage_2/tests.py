import datetime
from django.core.exceptions import ImproperlyConfigured
from django.core.files.base import ContentFile
from django.test import TestCase
from django_dropbox_storage_2.settings import DEFAULT_ROOT_FOLDER
from django_dropbox_storage_2.storage import DropboxStorage


class DropboxStorageTest(TestCase):
    def setUp(self):
        self.location = '/django_dropbox_storage_testing'
        self.storage = DropboxStorage(location=self.location)
        self.storage.base_url = '/test_media_url/'

    def tearDown(self):
        self.storage.delete(self.location)

    def test_no_access_token(self, *args):
        """
        Storage raises an exception if access token is empty.
        """
        with self.assertRaises(ImproperlyConfigured):
            DropboxStorage(token=None)

        with self.assertRaises(ImproperlyConfigured):
            DropboxStorage(token='')

    def test_default_root_folder(self, *args):
        """
        Storage uses default root folder if not provided.
        """
        storage = DropboxStorage(location=None)
        self.assertEqual(storage.location, DEFAULT_ROOT_FOLDER)

    def test_passing_location(self, *args):
        """
        Storage uses given location as root folder.
        """
        storage = DropboxStorage(location='/custom/root/folder')
        self.assertEqual(storage.location, '/custom/root/folder')

    def test_create_on_custom_location(self, *args):
        """
        Storage uses given location as root folder even on file creation.
        """
        CUSTOM_ROOT_FOLDER = '/custom/root/folder'

        storage = DropboxStorage(location=CUSTOM_ROOT_FOLDER)
        self.assertEqual(storage.location, CUSTOM_ROOT_FOLDER)

        f = storage.open('django_storage_test_exists', 'w')
        f.write('storage contents')
        f.close()
        self.assertTrue(storage.exists('django_storage_test_exists'))

        self.assertTrue(self.storage.exists(CUSTOM_ROOT_FOLDER + '/django_storage_test_exists'))

    def test_file_access_options(self):
        """
        Standard file access options are available, and work as expected.
        """
        self.assertFalse(self.storage.exists('django_storage_test'))
        f = self.storage.open('django_storage_test', 'w')
        f.write('storage contents')
        f.close()
        self.assertTrue(self.storage.exists('django_storage_test'))

        f = self.storage.open('django_storage_test', 'r')
        self.assertEqual(f.read(), 'storage contents')
        f.close()

        self.storage.delete('django_storage_test')

    def test_exists_folder(self):
        """
        Storage creates a folder.
        """
        self.assertFalse(self.storage.exists('django_storage_test_exists'))
        self.storage.client.files_create_folder(self.location + '/django_storage_test_exists')
        self.assertTrue(self.storage.exists('django_storage_test_exists'))
        self.storage.delete('django_storage_test_exists')
        self.assertFalse(self.storage.exists('django_storage_test_exists'))

    def test_listdir(self):
        """
        Storage returns a tuple containing directories and files.
        """
        self.assertFalse(self.storage.exists('django_storage_test_1'))
        self.assertFalse(self.storage.exists('django_storage_test_2'))
        self.assertFalse(self.storage.exists('django_storage_dir_1'))

        self.storage.save('django_storage_test_1', ContentFile('custom content'))
        self.storage.save('django_storage_test_2', ContentFile('custom content'))
        self.storage.client.files_create_folder(self.location + '/django_storage_dir_1')

        dirs, files = self.storage.listdir(self.location)
        self.assertEqual(set(dirs), set([u'django_storage_dir_1']))
        self.assertEqual(set(files),
                         set([u'django_storage_test_1', u'django_storage_test_2']))

        self.storage.delete('django_storage_test_1')
        self.storage.delete('django_storage_test_2')
        self.storage.delete('django_storage_dir_1')

    def test_file_delete(self):
        """
        Storage returns true if deletion was performed, false otherwise.
        """
        self.assertFalse(self.storage.exists('django_storage_test_delete'))
        f = self.storage.open('django_storage_test_delete', 'w')
        f.write('storage delete')
        f.close()
        self.assertTrue(self.storage.exists('django_storage_test_delete'))

        deleted = self.storage.delete('django_storage_test_delete')
        self.assertEqual(deleted, True)

        self.assertFalse(self.storage.exists('django_storage_test_delete'))

        deleted = self.storage.delete('django_storage_test_delete')
        self.assertEqual(deleted, False)

        self.assertFalse(self.storage.exists('django_storage_test_delete'))

    def test_write_readonly_file(self):
        """
        Storage raises an error when trying to write on a read-only file.
        """
        f = self.storage.open('django_storage_test_write_on_readonly', 'r')

        with self.assertRaises(AttributeError):
            f.write('read-only file')

        f.close()

    def test_get_available_name(self):
        """
        Storage auto adds a suffix to given name if the filename already exist.
        """
        query = 'django_storage_my_file'
        ext = '.txt'
        fn = query + ext

        self.assertFalse(self.storage.exists(fn))
        name = self.storage.get_available_name(fn)
        self.assertEqual(name, self.location + '/' + fn)

        f = self.storage.open(fn, 'w')
        f.write(query)
        f.close()

        self.assertTrue(self.storage.exists(fn))
        name = self.storage.get_available_name(fn)
        self.assertEqual(name, self.location + '/' + query + '_1' + ext)

    def test_file_size(self):
        """
        Storage returns a url to access a given file from the Web.
        """
        self.assertFalse(self.storage.exists('django_storage_test_size'))
        f = self.storage.open('django_storage_test_size', 'w')
        f.write('these are 18 bytes')
        f.close()
        self.assertTrue(self.storage.exists('django_storage_test_size'))

        f = self.storage.open('django_storage_test_size', 'r')
        self.assertEqual(f.size, 18)
        f.close()

        self.assertEqual(self.storage.size('django_storage_test_size'), 18)

        self.storage.delete('django_storage_test_size')

    def test_file_url(self):
        """
        Storage returns a url to access a given file from the Web.
        """
        self.assertFalse(self.storage.exists('django_storage_test_url'))
        f = self.storage.open('django_storage_test_url', 'w')
        f.write('storage url')
        f.close()
        self.assertTrue(self.storage.exists('django_storage_test_url'))

        self.assertTrue(self.storage.url('django_storage_test_url').startswith(
            'https://dl.dropboxusercontent.com/apitl'))

        self.storage.delete('django_storage_test_url')

    def test_file_modified_time(self):
        """
        Storage returns the time of latest change of given file from the Web.
        """
        f = self.storage.open('django_storage_test_modified_time', 'w')
        f.write('storage modified time')
        f.close()

        mt = self.storage.modified_time('django_storage_test_modified_time')
        self.assertIsInstance(mt, datetime.datetime)

        self.storage.delete('django_storage_test_modified_time')

    def test_file_accessed_time(self):
        """
        Storage returns the time of latest access to given file from the Web.
        """
        f = self.storage.open('django_storage_test_accessed_time', 'w')
        f.write('storage accessed time')
        f.close()

        at = self.storage.accessed_time('django_storage_test_accessed_time')
        self.assertIsInstance(at, datetime.datetime)

        self.storage.delete('django_storage_test_accessed_time')
