import time
import tweepy
import os
import praw
import requests
print("Logging into Twitter...")
consumer_key = "CONSUMERKEY"
consumer_secret = "CONSUMERSECRET"
access_token = "ACCESSTOKEN"
access_token_secret = "ACCESSTOKEN_SECRET"
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
auth.secure = True
api = tweepy.API(auth)
print("Logged in succesfully!")
def bot_login():
	print("Logging into reddit..")
	r = praw.Reddit(username = "YOUR_USERNAME", password = "YOURPASSWORD", client_id = "CLIENT_ID", client_secret = "CLIENT_SECRET", user_agent = "USERAGENT")
	print ("Logged in to reddit succesfully!")
	return r
def run_bot(r):
	print("Looking at hot posts in /r/DankMemes...")
	for submission in r.subreddit("DankMemes+Dank_Memes").stream.submissions(pause_after = 0):
		if ".jpg" in submission.url and submission.url not in posted_tweets:
			print("Found jpg on /r/DankMemes!")
			postitle = submission.title
			postimg = submission.url
			tweet_imagejpg(postimg,postitle)
			posted_tweets.append(submission.url)
			with open ("tweets_posted.txt","a") as f:
				f.write(submission.url + "\n")
			time.sleep(1)
		elif submission.url in posted_tweets:
			print("Picture already posted...")
			time.sleep(30)
		else:
			print("no picture...")
	print("sleeping for 20 seconds..")
	time.sleep(20)

def tweet_imagejpg(url, message):
	filename = "myimagesname.jpg"
	request = requests.get(url, stream=True)
	if request.status_code == 200:
		with open(filename, 'wb') as image:
			for chunk in request:
				image.write(chunk)

		api.update_with_media(filename, status=message)
		os.remove(filename)
		print("Tweeted picture!")
		time.sleep(30)
	else:
		print("Unable to download image")
def get_saved_tweets():
	if not os.path.isfile("tweets_posted.txt"):
		posted_tweets = []
	else:
		with open("tweets_posted.txt", "r") as f:
			posted_tweets = f.read()
			posted_tweets = posted_tweets.split("\n")
	return posted_tweets
r = bot_login()
posted_tweets = get_saved_tweets()
while True:
	try:
		run_bot(r)
	except:
		print("Unknown Error sleeping for 10s")
		time.sleep(10)
