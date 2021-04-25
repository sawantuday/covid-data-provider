from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk, requests #, pandas as pd
import time

class TweetService:

    def __init__(self):
        nltk.download('stopwords')
        nltk.download('punkt')

        towns, states = self.getTownList()
        self.states = states
        self.towns = towns
        
        puncts = ['.', ',', ':', '@', '#', '-']
        self.stopwords = stopwords.words('english') + puncts

        self.tweetList = None  # self.getProcessedTweets()
        self.lastFetched = 0  
        self.cacheTime = 300 # 5 minutes 

    def getTweets(self) -> list:
        # fetch tweet data from google sheets 
        jsonUrl = 'https://spreadsheets.google.com/feeds/cells/1cz2dSZWB9B_48Xxb8auM2dnPTzoM6tRGJWGH-MWvdg0/1/public/full?alt=json'
        response = requests.get(jsonUrl)
        results = response.json()
        rows = results['feed']['entry']

        # get tweets in a list 
        i = 4
        tweetList = []
        while i < len(rows):
            tweet = dict({
                'username': rows[i]['content']['$t'],
                'text': rows[i+1]['content']['$t'],
                'link': rows[i+2]['content']['$t'],
                'ts': rows[i+3]['content']['$t']
            })
            tweetList.append(tweet)
            i = i + 4

        return tweetList

    def getTownList(self):
        jsonUrl = 'https://spreadsheets.google.com/feeds/cells/1LMqd74dNT-4Dc5oy44tavvhHu1xKuyTVlssxxa1eTUg/1/public/full?alt=json'
        response = requests.get(jsonUrl)
        data = response.json()
        data = data['feed']['entry']

        townList = []
        stateList = []
        i = 4
        while i < len(data):
            town = data[i]['content']['$t']
            state = data[i+1]['content']['$t']
            i = i + 4
            townList.append(town.lower())
            stateList.append(state.lower())

        return townList, list(set(stateList))

    def cleanText(self, text) -> str:
        t = word_tokenize(text)
        tokens = [w.lower().replace('#', ' ') for w in t if w.lower() not in self.stopwords]
        return ' '.join(tokens)

    def isOxygen(self, text):
        return self.isAvailable(text) and 'oxygen' in text

    def isbeds(self, text):
        return 'bed' in text or 'beds' in text or 'hospital beds' in text or 'hospitalbeds' in text 

    def getLocation(self, text):
        words = [t for t in text.split(' ') if t in self.towns]
        return ' '.join(set(words))

    def getState(self, text):
        words = [t for t in text.split(' ') if t in self.states]
        return ' '.join(set(words))
        
    def isIcu(self, text):
        return self.isAvailable(text) and 'icu' in text

    def isAvailable(self, text):
        return 'available' in text

    def isNeeded(self, text):
        return 'needed' in text or 'required' in text

    def isVentilator(self, text):
        return self.isAvailable(text) and 'ventilator' in text

    def isFabifle(self, text):
        return self.isAvailable(text) and 'fabiflu' in text

    def isRemdesivir(self, text):
        return self.isAvailable(text) and 'remdesivir' in text

    def isFavipiravir(self, text):
        return self.isAvailable(text) and 'favipiravir' in text

    def isToclizumab(self, text):
        return self.isAvailable(text) and 'toclizumab' in text

    def isPlasma(self, text):
        return self.isAvailable(text) and 'plasma' in text

    def enrichTweetList(self, tweetList) -> list:
        for index, tweet in enumerate(tweetList):
            cleanedText = self.cleanText(tweet['text'])
            tweetList[index]['beds'] = self.isbeds(cleanedText)
            tweetList[index]['oxygen'] = self.isOxygen(cleanedText)
            tweetList[index]['state'] = self.getState(cleanedText)
            tweetList[index]['location'] = self.getLocation(cleanedText)
            tweetList[index]['icu'] = self.isIcu(cleanedText)
            tweetList[index]['ventilator'] = self.isVentilator(cleanedText)
            tweetList[index]['fabiflu'] = self.isFabifle(cleanedText)
            tweetList[index]['remdesivir'] = self.isRemdesivir(cleanedText)
            tweetList[index]['favipiravir'] = self.isFavipiravir(cleanedText)
            tweetList[index]['toclizumab'] = self.isToclizumab(cleanedText)
            tweetList[index]['plasma'] = self.isPlasma(cleanedText)

        return tweetList

    def getProcessedTweets(self) -> list:
        tweets = self.getTweets()
        return self.enrichTweetList(tweets)

    def getCachedTweets(self, start=0, end=50) -> list:
        t = int(time.time())
        if self.tweetList == None or t > self.lastFetched + self.cacheTime :
            self.tweetList = self.getProcessedTweets()
            self.lastFetched = t

        # TODO: how to use 'start' while sending data from end ?
        return self.tweetList[-end:]

    