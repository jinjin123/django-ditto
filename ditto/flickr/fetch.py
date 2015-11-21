import datetime
import pytz

import flickrapi
from flickrapi.exceptions import FlickrError

from .models import Account, User

# CLASSES HERE:
#
# FetchError
#
# UserMixin
#
# Fetch
#   FetchUser
#
# FlickrFetcher
#   UserFetcher
#
# Use a fetcher like:
#
#   fetcher = UserFetcher()
#   results = fetcher.fetch(url='https://www.flickr.com/photos/philgyford/')


class FetchError(Exception):
    pass


class UserMixin(object):

    def save_user(self, user, fetch_time):
        print(user)
        # Return User object.


class Fetch(object):
    """Parent class for children that will call the Flickr API to fetch data.

    Children should define their own methods for:
        TODO

    """
    # Will be an Account object, passed into init()
    account = None

    # Will be the FlickrAPI object for calling the Flickr API.
    api = None

    # Will be the UTC datetime that we fetch the results.
    fetch_time = None

    # Will be the results fetched from the API via FlickrAPI.
    results = []

    # Will be a list of all the Users/Photos/etc created/updated:
    objects = []

    # What we'll return for each account:
    return_value = {}

    # When fetching Photos or Users this will be the total amount fetched.
    results_count = 0

    def __init__(self, account):
        self.account = account

    def fetch(self):
        self._reset()

        if self.account.user:
            self.return_value['account'] = self.account.user.username
        elif self.account.pk:
            self.return_value['account'] = 'Account: %s' % str(self.account)
        else:
            self.return_value['account'] = 'Unsaved Account'

        if self.account.has_credentials():
            self.api = flickrapi.FlickrAPI(self.account.api_key,
                                self.account.api_secret, format='parsed-json')
            self._fetch_pages()
            self._post_fetch()
        else:
            self.return_value['success'] = False
            self.return_value['message'] = 'Account has no API credentials'

        self.return_value['fetched'] = self.results_count

        return self.return_value
        
    def _reset(self):
        self.fetch_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        self.results = []
        self.objects = []
        self.return_value = {}
        self.results_count = 0

    def _fetch_pages(self):
        try:
            self._call_api()
        except FetchError as e:
            self.return_value['success'] = False
            self.return_value['message'] = 'Error when calling API: %s' % e
        else:
            # If we've got to the last 'page' of tweet results, we'll receive
            # an empty list from the API.
            if (len(self.results) > 0):
                self._save_results()
                self._post_save()

            self.return_value['success'] = True
        return

    def _call_api(self):
        """Define in child classes.
        Should call self.api.a_function_name() and set self.results with the
        results.
        """
        raise FetchError("Children of the Fetch class should define their own _call_api() method.")

    
    def _save_results(self):
        """Define in child classes.
        Should go through self._results() and, probably, call
        self.save_user() or self.save_photo() for each one.
        """
        self.objects = []

    def _post_save(self):
        """Can optionally be defined in child classes.
        Do any extra things that need to be done after saving a page of data.
        """
        pass

    def _post_fetch(self):
        """Can optionally be defined in child classes.
        Do any extra things that need to be done after we've fetched all data.
        """
        pass


class FetchUser(UserMixin, Fetch):
    """Fetch and save info about a single user."""

    user_url = None

    def fetch(self, url=None):
        """
        url -- The Flickr URL owned by a user,
                eg 'https://www.flickr.com/photos/philgyford/8102921/'
        """
        self.user_url = url
        return super().fetch()

    def _call_api(self):
        "Get the User data from Flickr and save into self.results"

        # First, need to get the user's NSID using the URL we have:
        try:
            user = self.api.urls.lookupUser(url=self.user_url)
        except FlickrError as e:
            raise FetchError("Error when looking up user with URL '%s': %s" % (self.user_url, e))

        # Now we've got the NSID, get the user's info:
        try:
            info = self.api.people.getInfo(user_id=user['user']['id'])
        except FlickrError as e:
            raise FetchError("Error when getting info about User with id '%s': %s" % (user['user']['id'], e))

        self.results = [info['person']]

    def _save_results(self):
        user_obj = self.save_user(self.results[0], self.fetch_time)
        self.objects.append(user_obj)
        self.return_value['user'] = {'name': user_obj.name}
        self.results_count = 1


class FlickrFetcher(object):

    def __init__(self, username=None):
        """Keyword arguments:
        username -- of the one Account to get, or None for all Accounts.

        Raises:
        FetchError if passed a username there is no Account for.
        """
        self._set_accounts(username)

        # Will be a list of dicts that we return detailing succes/failure
        # results, one dict per account we've fetched for. eg:
        # [ {'account': 'thescreename', 'success': True, 'fetched': 200} ]
        self.return_values = []

    def fetch(self, **kwargs):
        """Fetch data for one or more Accounts.

        Returns:
        A list of dicts, one dict per Account, containing data about
        success/failure.
        """
        for account in self.accounts:
            accountFetcher = self._get_account_fetcher(account)
            return_value = accountFetcher.fetch(**kwargs)
            self._add_to_return_values(return_value)

        return self.return_values

    def _get_account_fetcher(self, account):
        """Should be changed for each child class.
        Should return an instance of a child of Fetch().

        Keyword arguments:
        account -- An Account object.
        """
        return Fetch()

    def _add_to_return_values(self, return_value):
        """Add return_value to the list in self.return_values."""
        self.return_values.append(return_value)

    def _set_accounts(self, username=None):
        """Sets self.accounts to all Accounts or just one.

        Keyword arguments:
        username -- of the one Account to get, or None for all Accounts.

        Raises:
        FetchError if passed a username there is no Account for, or if none
            of the requested account(s) are marked as is_active.
        """
        if username is None:
            accounts = Account.objects.filter(is_active=True)
            if (len(accounts) == 0):
                raise FetchError("No active Accounts were found to fetch.")
        else:
            try:
                accounts = [Account.objects.get(user__username=username)]
            except Account.DoesNotExist:
                raise FetchError("There is no Account in the database with a username of '%s'" % username)
            else:
                if accounts[0].is_active == False:
                    raise FetchError("The '%s' Account is marked as inactive." % username)

        self.accounts = accounts


class UserFetcher(FlickrFetcher):
    """Fetches data for a single Flickr user.
    Currently only accepts the URL of a page owned by that user. eg
    https://www.flickr.com/photos/philgyford/8102921/

    Usage:
        fetcher = UserFetcher()
        results = fetcher.fetch(url='https://www.flickr.com/philgyford')
    """
    def fetch(self, url=None):
        return super().fetch(url=url)

    def _get_account_fetcher(self, account):
        return FetchUser(account)

    def _set_accounts(self, username=None):
        super()._set_accounts(username=username)
        if len(self.accounts) > 0:
            self.accounts = [self.accounts[0]]

