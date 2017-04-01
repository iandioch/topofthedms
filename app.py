import csv
import random
import time
import tweepy
from urllib import request

AUTH_FILE = 'twitter_auth.hidden'
CHART_URL = 'https://spotifycharts.com/regional/global/daily/latest/download'
THEMED_WORDS_FILE = 'twitter_words.txt'
# number of minutes between tweets
TWEET_INTERVAL = 1
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

def load_themed_words():
    try:
        with open(THEMED_WORDS_FILE, 'r') as f:
            words = [word.strip() for word in f.readlines()]
            return words
    except Exception as e:
        print('Error loading themed word file:', e)
        return None

def generate_tweet(tracks, themed_words):
    track, artist = random.choice(tracks)
    theme_word = random.choice(themed_words)
    track_words = track.lower().split(' ')
    artist_words = artist.lower().split(' ')
    if len(track_words) == 1:
        # no good
        if len(artist_words) == 1:
            # this artist + track combo isn't useful, try another
            # this is very elegant code, don't @ me
            return generate_tweet(tracks, themed_words)
        n = random.randrange(len(artist_words))
        artist_words[n] = theme_word
    else:
        n = random.randrange(len(track_words))
        track_words[n] = theme_word
    return '"{}" - {}'.format(' '.join(track_words), ' '.join(artist_words))

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

    themed_words = load_themed_words()
    if themed_words is None:
        print('themed words is None')
        return

    while True:
        for _ in range(TWEETS_BEFORE_CHART_UPDATE):
            tracks = download_latest_chart()
            if tracks is None:
                time.sleep(TWEET_INTERVAL*60)
                break
            message = generate_tweet(tracks, themed_words)
            tweet(api, message)
            time.sleep(TWEET_INTERVAL*60)

if __name__ == '__main__':
    main()
