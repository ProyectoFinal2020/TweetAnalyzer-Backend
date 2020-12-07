from textblob import TextBlob


class TweetConverter:
    def __init__(self, language):
        self.language = language

    def getId(self, status):
        return status.id_str

    def getName(self, status):
        return status.user.name

    def getUsername(self, status):
        return status.user.screen_name

    def getTo(self, status):
        return status.in_reply_to_screen_name if status.in_reply_to_screen_name else ""

    def getText(self, status):
        return status.full_text

    def getRetweets(self, status):
        return status.retweet_count

    def getFavorites(self, status):
        return status.favorite_count

    def getReplies(self, status):
        return -1  # no esta disponible para el Cursor

    def getPermalink(self, status):
        return "https://twitter.com/{}/status/{}".format(status.user.screen_name, status.id_str)

    def getAuthorId(self, status):
        return status.user.id

    def getDate(self, status):
        return status.created_at

    def getFormattedDate(self, status):
        return status.created_at.strftime("%a %b %d %H:%M:%S %z %Y")

    def getHashtags(self, status):
        hashtags = ""
        if status.entities is not None and len(status.entities) > 0:
            hashtags = " ".join("#" + str(hashtag["text"]) for hashtag in status.entities['hashtags'])
        return hashtags

    def getMentions(self, status):
        mentions = ""
        if status.entities is not None and len(status.entities) > 0:
            mentions = " ".join(str(mention["screen_name"]) for mention in status.entities['user_mentions'])
        return mentions

    def getUrls(self, status):
        urls = ""
        if status.entities is not None and len(status.entities) > 0:
            urls = " ".join([tweet_urls['url'] for tweet_urls in
                             status.entities['urls']])
        return urls

    def getGeo(self, status):
        return str(status.geo['coordinates'][0]) + ', ' + str(status.geo['coordinates'][1]) \
            if status.geo and status.geo['coordinates'] else ""

    def getProfileImgUrl(self, status):
        return status.user.profile_image_url

    def getEmotion(self, status):
        blob = TextBlob(status.full_text)
        if self.language == 'es':
            blob = blob.translate(to='en')
        return blob.sentiment
