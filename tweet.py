import sentiment_mod as s
from bad_words_dict import russophobic_words as badWords

from tweepy import Stream
from tweepy import OAuthHandler, API
from tweepy.streaming import StreamListener

import json, time




#consumer key, consumer secret, access token, access secret.
ckey="cgVVTVDVXXrtxqDIochB2B1fP"
csecret="8HVpfSaJh9BmLWEu7cjPQPHHFWGN7ngCCqMFDy2HoiGKPtc61r"
atoken="933017676666015744-gGxDxambk7PntsXd43GiytavqXiJadF"
asecret="6fORYTHiM5BpGPfnCXCKUAkD81F2T69hRl7o62Gg9hi31"

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        avoid = ["anti-russia", "@reprohrabacher","@berniesanders", "usa backed", "schroeder","pence","democrats",
                 'manafort',"gorsuch","obama","porn","skater","slutty","teen"]
        publish = True
        tweet = all_data["text"]
        id = all_data["id"]
        retweeted = all_data["retweeted"]
        for word in avoid:
                if word in tweet.lower():
                    publish = False
                
        if retweeted or 'RT @' in tweet:
            publish = False
 
        try:
            
            sentiment_value, confidence = s.sentiment(tweet)
            kostyl_polarity = 0
            
            for x in badWords.keys():
                if x in tweet:
                    kostyl_polarity += badWords[x]/10
                    
            if (publish == True) and ((str(sentiment_value) == 'neg' and confidence*100>=90) or (str(sentiment_value) == 'neg' and confidence*100>=50 and kostyl_polarity<-0.6)):
            
                print(tweet, sentiment_value, confidence, kostyl_polarity)
                print()
                twitter_client.retweet(id)
                time.sleep(4)
                                  
        except Exception as e:
            print(e)
        
        
        return True

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitter_client = API(auth)


twitterStream = Stream(auth, listener())
twitterStream.filter(track=["Russia","Russiagate", "Putin", "Russian","Kremlin","russkies","ruskies","rooskies", "RussiaTaliban", "Russian spies"])
