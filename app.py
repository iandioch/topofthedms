import csv
import random
import re
import time
import tweepy
from urllib import request, parse

AUTH_FILE = 'twitter_auth.hidden'
CHART_URL = 'https://spotifycharts.com/regional/global/daily/latest/download'
THEMED_WORDS_FILE = 'twitter_words.txt'
STOP_WORDS_FILE = 'stop_words.txt'
# number of minutes between tweets
TWEET_INTERVAL = 15
# number of tweets to send before refreshing the track list
TWEETS_BEFORE_CHART_UPDATE = (24*60)//TWEET_INTERVAL


def download_latest_chart():
    """Returns a list of (track, artist) tuples"""
    try:
        req = request.urlopen(CHART_URL)
        chart = req.read().decode('utf-8').split('\n')
        reader = csv.reader(chart)
        next(reader)  # skip the titles of columns
        tracks = [(row[1], row[2]) for row in reader if len(row) > 0]
        return tracks
    except Exception as e:
        print('Error fetching chart:', e)
        return None


def load_file(path):
    try:
        with open(path, 'r') as f:
            words = [word.lower().strip() for word in f.readlines()]
            return words
    except Exception as e:
        print('Error loading file "{}": "{}"'.format(path, e))
        return None


def load_themed_words():
    return load_file(THEMED_WORDS_FILE)


def load_stop_words():
    return load_file(STOP_WORDS_FILE)


def replace_non_stop_word(full_word, theme_word, stop_words):
    words = re.split(r'\s+|[][(),-]\s*', full_word)
    print(stop_words)
    for _ in range(len(words)):
        n = random.randrange(len(words))
        if words[n] not in stop_words:
            return full_word.replace(words[n], theme_word)
    return None


def generate_tweet(tracks, themed_words, stop_words):
    track, artist = random.choice(tracks)
    track = track.lower()
    artist = artist.lower()
    theme_word = random.choice(themed_words)
    track_words = track.split(' ')
    artist_words = artist.split(' ')
    if len(track_words) == 1:
        # no good
        # this artist + track combo isn't useful, try another
        # this is very elegant code, don't @ me
        return generate_tweet(tracks, themed_words, stop_words)
    else:
        # can use track name (preferred)
        t = replace_non_stop_word(track, theme_word, stop_words)
        if t is None:
            return generate_tweet(tracks, themed_words, stop_words)
        track = t
    return "'{}' - {}".format(track, artist)


def tweet(api, message):
    print('Tweeting:', message)
    try:
        api.update_status(status=message)
    except Exception as e:
        print('Failure during tweet:', e, type(e))


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

    stop_words = load_stop_words()
    if stop_words is None:
        print('stop words is None')
        return
    stop_words = set(stop_words)

    while True:
        for _ in range(TWEETS_BEFORE_CHART_UPDATE):
            tracks = download_latest_chart()
            if tracks is None:
                time.sleep(TWEET_INTERVAL*60)
                break
            message = generate_tweet(tracks, themed_words, stop_words)
            tweet(api, message)
            time.sleep(TWEET_INTERVAL*60)


if __name__ == '__main__':
    main()
