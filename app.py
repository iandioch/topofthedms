import csv
import random
import time
import tweepy
from urllib import request

AUTH_FILE = 'twitter_auth.hidden'
CHART_URL = 'https://spotifycharts.com/regional/global/daily/latest/download'
# number of minutes between tweets
TWEET_INTERVAL = 3
# number of tweets to send before refreshing the track list
TWEETS_BEFORE_CHART_UPDATE = (24*60)//TWEET_INTERVAL

def download_latest_chart():
    """Returns a list of (track, artist) tuples"""
    try:
        req = request.urlopen(CHART_URL)
        chart = req.read().decode('utf-8').split('\n')
        reader = csv.reader(chart)
        next(reader) # skip the titles of columns
        tracks = [(row[1], row[2]) for row in reader if len(row) > 0]
        return tracks
    except Exception as e:
        print('Error fetching chart:', e)
        return None

def generate_tweet(tracks):
    track, artist = random.choice(tracks)
    return '"{}" - {}'.format(track, artist)

def tweet(api, message):
    print('Tweeting:', message)
    try:
        api.update_status(message)
    except Exception as e:
        print('Failure during tweet:', e)

def main():
    api = None
    with open(AUTH_FILE, 'r') as f:
        data = [line.strip() for line in f.readlines()]
        auth = tweepy.OAuthHandler(data[0], data[1])
        auth.set_access_token(data[2], data[3])
        api = tweepy.API(auth)
    if api is None:
        print('api is None')
        return

    while True:
        for _ in range(TWEETS_BEFORE_CHART_UPDATE):
            tracks = download_latest_chart()
            if tracks is None:
                time.sleep(TWEET_INTERVAL*60)
                break
            message = generate_tweet(tracks)
            tweet(api, message)
            time.sleep(TWEET_INTERVAL*60)

if __name__ == '__main__':
    main()
