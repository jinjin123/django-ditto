from ...fetch import TweetsFetcher
from ._update_twitter import UpdateTwitterCommand


class Command(UpdateTwitterCommand):
    """Fetches data for all Twitter Tweets in the DB, updating their info.

    Specify an account to use its API credentials:
    ./manage.py update_twitter_tweets --account=philgyford
    """

    help = "Fetches the latest data about each Twitter Tweet"

    updated_noun = 'Tweet'

    def fetch(self, screen_name):
        return TweetsFetcher(screen_name=screen_name).fetch()

