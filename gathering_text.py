import tweepy
import re
import emoji
import key
from google.cloud import language_v1

API_KEY = key.API_KEY
API_KEY_SECRET = key.API_KEY_SECRET
ACCESS_TOKEN = key.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = key.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
client = language_v1.LanguageServiceClient()

results = []
count = 0
allscore = 0.0
avg = 0.0

emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth      
      |
      [\)\]\(\[dDpP/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8]                     # eyes
      [<>]?
    )"""

def give_emoji_free_text(text): 
    return emoji.get_emoji_regexp().sub(r'', text)

def cleaning_text(text):
    text = give_emoji_free_text(text)
    text = re.sub(emoticon_string, repl = '', string = text) # remove emoji

    pattern = 'https://t.co/+\\S+' # remove t.co link
    text = re.sub(pattern = pattern, repl = '', string = text)

    pattern = '@\\S+' # remove mention
    text = re.sub(pattern = pattern, repl = '', string = text)

    pattern = '#\\S+' # remove hashtag
    text = re.sub(pattern = pattern, repl = '', string = text)

    pattern = '\\n+'
    text = re.sub(pattern = pattern, repl = '', string = text)

    pattern = '\\xa0+'
    text = re.sub(pattern = pattern, repl = ' ', string = text)

    pattern = ' +' 
    text = re.sub(pattern = pattern, repl = ' ', string = text)

    return(text)

def get_avg_sentimentscore(score):
    global count, allscore
    count = count + 1
    allscore = allscore + score


def get_twitter_text(keyword):
    global avg
    for tweet in tweepy.Cursor(api.search, q=keyword, lang='en', include_entities=False, tweet_mode='extended').items(100):
        if "RT" not in tweet.full_text:
            document = language_v1.Document(content=cleaning_text(tweet.full_text), type_=language_v1.Document.Type.PLAIN_TEXT)
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
            # result.append([cleaning_text(tweet.full_text), sentiment.score, sentiment.magnitude])
            result = {'text': cleaning_text(tweet.full_text), 'sentimentscore': sentiment.score}

            if sentiment.score != 0:
                get_avg_sentimentscore(sentiment.score)

            results.append(result)
    avg = allscore / count
    return results

get_twitter_text('bts')
print(results)
print(avg, count, allscore)
