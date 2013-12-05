# To run this, go to the terminal and type: 
# python tweetStream.py <keywords> 


# _________________________ Started with code from: 
# http://answers.oreilly.com/topic/2605-how-to-capture-tweets-in-real-time-with-twitters-streaming-api/

# -*- coding: utf-8 -*-

import sys
import tweepy
import webbrowser
import json 
import time


def get_parser():
    import argparse
    parser = argparse.ArgumentParser(description='Search the Twitter stream for one or more keywords')
    parser.add_argument('--timeout', type=int, help='how long to collect tweets for (s)', default=None)
    parser.add_argument('keyword', nargs='+', help='keywords to search for')
    return parser

# Query terms
parser = get_parser()
args = parser.parse_args()
Q = args.keyword

# Load credentials from credentials.cfg
import cred
credentials = cred.read_credentials()

CONSUMER_KEY = credentials['consumer_key']
CONSUMER_SECRET = credentials['consumer_secret']

# Get these values from the "My Access Token" link located in the
# margin of your application details, or perform the full OAuth
# dance.

ACCESS_TOKEN = credentials['access_token_key']
ACCESS_TOKEN_SECRET = credentials['access_token_secret'] 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

## added by CC as a place to output tweets to a file, currently this file isn't ever closed
outputfile = open('tweets.out', 'w')

class TimedStreamListener(tweepy.StreamListener):
    """A StreamListener that stops collecting data after a specified timeout. Here's the idea.

    1) record the time the stream listener is created. This is the start time.

    2) every time we get a new data packet, process it and then see if we've
       reached the timeout. If so, return False to signal stop.

    HOWEVER, this doesn't handle the case where no data for our search term
    shows up once the timeout has been reached. The on_data function will never
    be called. So, we ALSO use an HTTP timeout in the enclosing Stream object.
    That timeout says "if the HTTP Stream has not received data for X seconds,
    throw an exception."
    
    Note that if we use an HTTP timeout equal to the specified timeout, the
    worst case is that we will actually wait 2*timeout seconds. Suppose we get
    a data package at (start + timeout - epsilon). Then the on_data timeout
    check will fail, so we won't stop. Then we wait another timeout seconds for
    HTTP timeout, and fail. This brings us basically to start + 2*timeout.

    To make a better approximation, use the HTTP timeout of something like 10%
    of timeout. That way we can only be 10% off, i.e., wait 1.1 * timeout
    instead of 2*timeout.

    The code below also includes a min(1 second, timeout) minimum HTTP sleep.
    In other words, we generally want the HTTP timeout to be at least 1 second
    because otherwise we'll hit the on_timeout function repeatedly and will
    keep killing the connection to Twitter and reconnecting."""

    def __init__(self, timeout=None):
        self.timeout = timeout
        self.start = time.time()
        tweepy.StreamListener.__init__(self)

    def on_data(self, raw_json):
        """This function is called whenever data (in the form of JSON) from
        Twitter is received. Here we intercept the data and log it, then pass
        it up to the super-class to be handled as usual.
        """
        outputfile.write(raw_json + '\n')
        print raw_json
        tweepy.StreamListener.on_data(self, raw_json)
        if self.timeout and (time.time() - self.start) > self.timeout:
            print >> sys.stderr, 'stopping because timeout reached...'
            return False

    def on_timeout(self):
        if self.timeout and (time.time() - self.start) > self.timeout:
            print >> sys.stderr, 'stopping because no data for timeout...'
            return False

# Create a streaming API and set a timeout value as described in TimedStreamListener above.
http_timeout_cushion = min(1.5, args.timeout)
http_timeout = max(http_timeout_cushion, args.timeout * 0.1)
streaming_api = tweepy.streaming.Stream(auth, TimedStreamListener(timeout=args.timeout), timeout=http_timeout)

# Optionally filter the statuses you want to track by providing a list
# of users to "follow".
print >> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),)
streaming_api.filter(follow=None, track=Q)
