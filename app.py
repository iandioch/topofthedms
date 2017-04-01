import tweepy

AUTH_FILE = 'twitter_auth.hidden'

def tweet(api, message):
    api.update_status(message)

def main():
    with open(AUTH_FILE, 'r') as f:
        data = [line.strip() for line in f.readlines()]
        auth = tweepy.OAuthHandler(data[0], data[1])
        auth.set_access_token(data[2], data[3])
        api = tweepy.API(auth)
        print(api)
        tweet(api, 'help')

if __name__ == '__main__':
    main()
