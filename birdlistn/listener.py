import gevent

from cloudly.pubsub import RedisWebSocket
from cloudly.tweets import Tweets, StreamManager, keep
from cloudly import logger

from birdlistn.config import tweet_channel, metadata_channel

log = logger.init(__name__)
channels = {
    tweet_channel: RedisWebSocket(tweet_channel),
    metadata_channel: RedisWebSocket(metadata_channel),
}
is_running = False


def process_tweets(tweets):
    channels[tweet_channel].publish(keep(['coordinates', 'lang'], tweets),
                                    "tweets")
    return len(tweets)


def process_metadata(metadata):
    channels[metadata_channel].publish(metadata)


def run():
    log.info("Starting Twitter stream manager.")
    streamer = StreamManager('locate', process_tweets, process_metadata,
                             is_queuing=False)
    tweets = Tweets()
    streamer.run(tweets.with_coordinates(), stop)
    log.info("Twitter stream manager has stopped.")


def start():
    global is_running
    if not is_running:
        gevent.spawn(run)
        is_running = True


def stop(stopping=None):
    """This function is called periodically by the StreamManager to check if it
    should stop.
    """
    global is_running
    if stopping:
        log.info("Stopping Twitter stream manager.")
        is_running = False
    return not is_running
