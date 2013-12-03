# To run this, go to the terminal and type: 
# python tweetStream.py <keywords> 


# _________________________ Started with code from: 
# http://answers.oreilly.com/topic/2605-how-to-capture-tweets-in-real-time-with-twitters-streaming-api/

# -*- coding: utf-8 -*-

import sys
import tweepy
import webbrowser
import json 


def get_parser():
    import argparse
    parser = argparse.ArgumentParser(description='Search the Twitter stream for one or more keywords')
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

# Note: Had you wanted to perform the full OAuth dance instead of using
# an access key and access secret, you could have uses the following 
# four lines of code instead of the previous line that manually set the
# access token via auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET).
# 
# auth_url = auth.get_authorization_url(signin_with_twitter=True)
# webbrowser.open(auth_url)
# verifier = raw_input('PIN: ').strip()
# auth.get_access_token(verifier)

## Note from CC - this might be the piece that is now deprecated.

## added by CC as a place to output tweets to a file, currently this file isn't ever closed
outputfile = open('tweets.out', 'w')

class CustomStreamListener(tweepy.StreamListener):

    def on_data(self, raw_json):
        """This function is called whenever data (in the form of JSON) from
        Twitter is received. Here we intercept the data and log it, then pass
        it up to the super-class to be handled as usual.
        """
        outputfile.write(raw_json + '\n')
        print raw_json
        tweepy.StreamListener.on_data(self, raw_json)

    def on_status(self, status):
        
        # We'll simply print some values in a tab-delimited format
        # suitable for capturing to a flat file but you could opt 
        # store them elsewhere, retweet select statuses, etc.


        try:
            #print "%s\t%s\t%s\t%s" % (status.text, 
            #                          status.author.screen_name, 
            #                          status.created_at, 
            #                          status.source,)
            pass
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

# Create a streaming API and set a timeout value of 60 seconds.

streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)

# Optionally filter the statuses you want to track by providing a list
# of users to "follow".

print >> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),)

streaming_api.filter(follow=None, track=Q)
