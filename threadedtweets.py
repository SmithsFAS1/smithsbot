#!/usr/bin/env python
#  
#   Just an example of creating a tweet thread from a script
#   Tweet something, get the tweet ID, store it, then reference it
#   in the follow-up tweet to thread it. Repeat.
#
#   This example is just uploading the same image every time, threaded to the previous tweet
#   with a date difference in the tweet (it has been X days since...)
#
#   -Smiths

import sys
from twython import Twython
import datetime
import sys
import json
import os

# your twitter consumer and access information goes here
# note: these are garbage strings and won't work
apiKey = 'pog4sjsAfk3k3gL2ejaRaa'
apiSecret = 'asdkljlkadjgklnreoighrevn3oru2938ry32'
accessToken = '371868721-RsodgvnesfweweFEFseCsec'
accessTokenSecret = 'CSDBJDRW383fcjqdsdcn231pfldmaa'

#variable for text file that will store the tweet ID. if it doesn't exist, will assume first tweet in thread
LASTTWEETFILE = 'FULL PATH TO FILE' #e.g. - /home/user/lasttweet.txt

#-------------------------------------------------
# Where we define what we want to tweet
#
# TWEETSTRING = what you want to tweet. can be modified to be anywhere in case you're doing things before generating the tweet's words
# e.g. - getting a date duration or needing a dynamic variable [uploading something to hosting site with an URL returned]
# in this example, we'll get the duration of time since Herman Cain was murdered - 7/30/2020 10:26AM

data1 = datetime.datetime.now()  #day today
data2 = datetime.datetime(2020,7,30,10,26) #date and time the Zombie Cain account tweeted he was killed
diff = data1 - data2 #time between the dates
duration_in_s = diff.total_seconds() #break it down
days = divmod(duration_in_s, 86400) #get the days
hours = divmod(days[1], 3600) #hours too in case you want them

#the string that will be tweeted
TWEETSTRING = "It's been %s days since Herman Cain was murdered\r\n" % (int(days[0])) #%s in string filled in by the int() of the date difference

#---------------------------------------------------

#check if we're threading - OLDTWEET will either be blank or fetch the ID from LASTTWEETFILE
OLDTWEET = ''
if (os.path.exists(LASTTWEETFILE)):
    with open(LASTTWEETFILE, 'r') as file:
        OLDTWEET = file.read().replace('\n', '') #get the ID from the file


#Twython time - log into Twitter with creds
api = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

#in this case, we're tweeting an image with the tweet. Have to define path to it and upload to twitter to start
IMAGEFILE = 'FULL PATH TO IMAGE' # e.g. - /home/user/image.jpg
PHOTO = open(IMAGEFILE, 'rb')
response = api.upload_media(media=PHOTO) #upload image, get 'response' from twitter which is needed (response['media_id'])

if len(OLDTWEET) > 0:
    a = api.update_status(status=TWEETSTRING, in_reply_to_status_id=OLDTWEET, media_ids=[response['media_id']]) #in_reply_to_status_id = thread
else:
    a = api.update_status(status=TWEETSTRING, media_ids=[response['media_id']])

#get all the stuff back from Twitter - we need the new Tweet's ID (tid) to put into our LASTTWEETFILE
json_str = json.dumps(a)
resp = json.loads(json_str)
tid = resp['id'] #the ID of the tweet that just posted
text_file = open(LASTTWEETFILE, "w")
n = text_file.write(str(tid)) #put it in the file
text_file.close()

print("Tweeted: " + TWEETSTRING + "\r\n")
