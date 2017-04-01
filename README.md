# Top of the DMs

A silly twitter bot that you can see in action at [@topofthedms](https://twitter.com/topofthedms).

It takes popular song titles and artists, and replaces one of the words in them with a Twitter-related word (eg. "DM", "subtweet", etc.).

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">&#39;block yourself&#39; - justin bieber</p>&mdash; Top of the DMs (@topofthedms) <a href="https://twitter.com/topofthedms/status/848012279664791552">April 1, 2017</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

- [spotifycharts.com](https://spotifycharts.com)'s CSV link is used to get the most popular songs every 24 hours.
- A list of stop words was taken from [xpo6.com](http://xpo6.com/list-of-english-stop-words/) to try and only replace non-grammatical words with the Twitter words.
- It uses [tweepy](https://github.com/tweepy/tweepy).
