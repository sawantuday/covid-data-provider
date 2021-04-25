from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk, requests #, pandas as pd

nltk.download('stopwords')
nltk.download('punkt')

# states or UT and towns 
states = ["Uttar Pradesh", "Gujarat", "Delhi", "Kerala", "Karnataka", "West Bengal", "Maharashtra", "Madhya Pradesh", "Uttarakhand", "Andhra Pradesh", 
          "Odisha", "Tamil Nadu", "Bihar", "Assam", "Telangana", "Tripura", "Chhattisgarh", "Rajasthan", "Jharkhand", "Haryana", "Andhrapradesh", 
          "Punjab", "Haryana", "Himachal Pradesh", "Andhra pradesh", "Jammu and Kashmir", "Puducherry", "Nagaland", "Manipur", "Mizoram", "Goa", 
          "Arunachal Pradesh", "Meghalaya", "Andaman and Nicobar Islands", "Dadra and Nagar Haveli"]
# following list is to address states with two words in name 
states = states + ['uttar', 'pradesh', 'bengal', 'madhya', 'andhra', 'tamil', 'nadu', 'Himachal', 'Jammu', 'Kashmir', 'Arunachal', 'Dadra', 
                   'Nagar', 'Haveli', 'Andaman', 'Nicobar']
states = [s.lower() for s in states]
towns = getTownList()

puncts = ['.', ',', ':', '@', '#', '-']
stopList = stopwords.words('english') + puncts

cachedTweets = None

def getTweets() -> list:
  # fetch tweet data from google sheets 
  jsonUrl = 'https://spreadsheets.google.com/feeds/cells/1LMqd74dNT-4Dc5oy44tavvhHu1xKuyTVlssxxa1eTUg/2/public/full?alt=json'
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

def getTownList():
  jsonUrl = 'https://spreadsheets.google.com/feeds/cells/1LMqd74dNT-4Dc5oy44tavvhHu1xKuyTVlssxxa1eTUg/1/public/full?alt=json'
  response = requests.get(jsonUrl)
  data = response.json()
  data = data['feed']['entry']

  townList = []
  i = 0
  while i < len(data):
    town = data[i]['content']['$t']
    i = i + 4
    townList.append(town.lower())

  return townList

def cleanText(text) -> str:
  t = word_tokenize(text)
  tokens = [w.lower().replace('#', ' ') for w in t if w.lower() not in stopList]
  return ' '.join(tokens)

def isOxygen(text):
  return isAvailable(text) and 'oxygen' in text

def isbeds(text):
  return 'bed' in text or 'beds' in text or 'hospital beds' in text or 'hospitalbeds' in text 

def getLocation(text):
  words = [t for t in text.split(' ') if t in towns]
  return ' '.join(set(words))

def getState(text):
  words = [t for t in text.split(' ') if t in states]
  return ' '.join(set(words))
  
def isIcu(text):
  return isAvailable(text) and 'icu' in text

def isAvailable(text):
  return 'available' in text

def isNeeded(text):
  return 'needed' in text or 'required' in text

def isVentilator(text):
  return isAvailable(text) and 'ventilator' in text

def isFabifle(text):
  return isAvailable(text) and 'fabiflu' in text

def isRemdesivir(text):
  return isAvailable(text) and 'remdesivir' in text

def isFavipiravir(text):
  return isAvailable(text) and 'favipiravir' in text

def isToclizumab(text):
  return isAvailable(text) and 'toclizumab' in text

def isPlasma(text):
  return isAvailable(text) and 'plasma' in text

def enrichTweetList(tweetList) -> list:
  for index, tweet in enumerate(tweetList):
    cleanedText = cleanText(tweet['text'])
    tweetList[index]['beds'] = isbeds(cleanedText)
    tweetList[index]['oxygen'] = isOxygen(cleanedText)
    tweetList[index]['state'] = getState(cleanedText)
    tweetList[index]['location'] = getLocation(cleanedText)
    tweetList[index]['icu'] = isIcu(cleanedText)
    tweetList[index]['ventilator'] = isVentilator(cleanedText)
    tweetList[index]['fabiflu'] = isFabifle(cleanedText)
    tweetList[index]['remdesivir'] = isRemdesivir(cleanedText)
    tweetList[index]['favipiravir'] = isFavipiravir(cleanedText)
    tweetList[index]['toclizumab'] = isToclizumab(cleanedText)
    tweetList[index]['plasma'] = isPlasma(cleanedText)

  return tweetList

def getProcessedTweets() -> list:
    tweets = getTweets()
    return enrichTweetList(tweets)

def getCachedTweets(start=0, end=50) -> list:
    if cachedTweets == None:
        cachedTweets = getProcessedTweets()
    # TODO: how to use 'start' while sending data from end ?
    return cachedTweets[-end]

# TODO: add stemming to improve detection and matching ratio 

# 31351

if __name__ == "__main__":
    tweets = getCachedTweets()
    print(tweets)

