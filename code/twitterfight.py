
DEFAULT_TIMEOUT = 10  # in seconds

class TwitterFight:
    
    def __init__(self, searchArg1, searchArg2, timeout = DEFAULT_TIMEOUT):
        self.result = [0, 0]
        self.done = False
        self.arg1 = searchArg1
        self.arg2 = searchArg2
        self.arg1_count = 0
        self.arg2_count = 0
        # start tweepy stream
        # on status, figure out which searchArg it is, count it to that one
        # wait 10 seconds
        # end tweepy stream
        # set self.done = True
    
    def result(self):
        # could modify so that we always get most recent results so we can visualize
        # to "watch" the bars on the graph go, more like a race
        if self.done:
            return self.result
        return None

class KeywordSearch:
    def __init__(self, keywords):
        self.keywords = keywords
        # start tweepy filter stream
        # write to file
        
    def mostRecent(self, num =1 ):
        # return the last num tweets in the file
        return None
    
    def allTweets(self):
        # return all tweets so far


'''
These objects should contain whatever info is needed to plot on a map the right way.
'''
class GeoCoords:
    def __init__(self, lat, longi):
        self.lat = lat
        self.longi = longi

class GeoBounds:
    def __init__(self, what, here):
        self.dunno = dontknow

# given tweet json, return coords
def Geolocate(tweet_json):
    # given tweet, if it has no location, return None
    # if it has geocoordinates, return a GeoCoords object
    # if it has geobounary, return a GeoBounds object
    # if it has a region/city, return a corresponding city

def 
