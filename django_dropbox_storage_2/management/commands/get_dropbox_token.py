# Original authors: Andres Torres and Maximiliano Cecilia

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand, CommandError
from dropbox import DropboxOAuth2FlowNoRedirect

from django_dropbox_storage_2.settings import CONSUMER_KEY, CONSUMER_SECRET


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not (CONSUMER_KEY and CONSUMER_SECRET):
            raise ImproperlyConfigured("To use this tool you have to set "
                                       "'settings.DROPBOX_CONSUMER_KEY' and "
                                       "'settings.DROPBOX_CONSUMER_SECRET'.")

        auth_flow = DropboxOAuth2FlowNoRedirect(CONSUMER_KEY, CONSUMER_SECRET)

        authorize_url = auth_flow.start()
        self.stdout.write('1. Go to: {}'.format(authorize_url))
        self.stdout.write('2. Click "Allow" (you might have to log in first).')
        self.stdout.write('3. Copy the authorization code.')
        auth_code = raw_input("Enter the authorization code here: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
            token = oauth_result.access_token
            self.stdout.write("DROPBOX_ACCESS_TOKEN = '{}'".format(token))
        except Exception as e:
            raise CommandError('Error: {}'.format(e))
