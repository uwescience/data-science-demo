import sys
import tweepy
import webbrowser
import json 
import time

# Load credentials from credentials.cfg
import cred
credentials = cred.read_credentials()

CONSUMER_KEY = credentials['consumer_key']
CONSUMER_SECRET = credentials['consumer_secret']

ACCESS_TOKEN = credentials['access_token_key']
ACCESS_TOKEN_SECRET = credentials['access_token_secret'] 

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

DEFAULT_TIMEOUT = 10  # in seconds

class TwoArgTimedStreamListener(tweepy.StreamListener):
    
    def __init__(self, arg1, arg2, score, timeout=None):
        self.timeout = timeout
        self.start = time.time()
        self.arg1 = arg1.lower()
        self.arg2 = arg2.lower()
        self.score = score
        tweepy.StreamListener.__init__(self)

    def on_data(self, raw_json):
        """This function is called whenever data (in the form of JSON) from
        Twitter is received. Here we intercept the data and log it, then pass
        it up to the super-class to be handled as usual.
        """
        data = json.loads(raw_json)
        # print data['text']
        if 'text' in data:
            text = data['text'].lower()
            if self.arg1 in text:
                self.score[0] += 1
                print 'arg1 ' + str(self.score[0])
            if self.arg2 in text:
                self.score[1] += 1
                print 'arg2 ' + str(self.score[1])
        
        tweepy.StreamListener.on_data(self, raw_json)
        if self.timeout and (time.time() - self.start) > self.timeout:
            print >> sys.stderr, 'stopping because timeout reached...'
            return False

    def on_timeout(self):
        if self.timeout and (time.time() - self.start) > self.timeout:
            print >> sys.stderr, 'stopping because no data for timeout...'
            return False



class TwitterFight:
 
    def __init__(self, searchArg1, searchArg2, timeout = DEFAULT_TIMEOUT):
        self.searchArg1 = searchArg1
        self.searchArg2 = searchArg2
        self.timeout = timeout
        self.Q = [self.searchArg1, self.searchArg2]

        self.score = [0,0]

        http_timeout_cushion = min(1.5, self.timeout)
        http_timeout = max(http_timeout_cushion, self.timeout * 0.1)

        streaming_api = tweepy.streaming.Stream(auth, TwoArgTimedStreamListener(self.searchArg1, self.searchArg2, self.score, self.timeout), timeout=http_timeout)
        streaming_api.filter(follow=None, track=self.Q)

    def final_score(self):
        return [{'label': self.searchArg1, 'value': self.score[0]},
                {'label': self.searchArg2, 'value': self.score[1]}]

if __name__ == "__main__":
    f = TwitterFight('Seattle', 'Bieber', 30)
    print f.score
    print f.final_score()
