from ...entities.userStreamingTweets import UserStreamingTweets
from flask_login import current_user


class TweetBuilder:
    def __init__(self, converter):
        self.converter = converter

    def generateTweet(self, status, topic_title):
        id = self.converter.getId(status)
        name = self.converter.getName(status)
        username = self.converter.getUsername(status)
        to = self.converter.getTo(status)
        text = self.converter.getText(status)
        retweets = self.converter.getRetweets(status)
        favorites = self.converter.getFavorites(status)
        replies = self.converter.getReplies(status)
        permalink = self.converter.getPermalink(status)
        author_id = self.converter.getAuthorId(status)
        date = self.converter.getDate(status)
        formatted_date = self.converter.getFormattedDate(status)
        hashtags = self.converter.getHashtags(status)
        mentions = self.converter.getMentions(status)
        urls = self.converter.getUrls(status)
        geo = self.converter.getGeo(status)
        img_url = self.converter.getProfileImgUrl(status)
        sent = self.converter.getEmotion(status)

        return UserStreamingTweets(
            user_id=current_user.id, topic_title=topic_title, id=id, name=name, username=username, to=to, text=text,
            retweets=retweets, favorites=favorites, replies=replies, permalink=permalink, author_id=author_id,
            date=date, formatted_date=formatted_date, hashtags=hashtags, mentions=mentions, geo=geo, urls=urls,
            img_url=img_url, polarity=sent.polarity, subjectivity=sent.subjectivity
        )

    def generateTweetDict(self, status, topic_title):
        tweet = dict()
        tweet['id'] = self.converter.getId(status)
        tweet['topic_title'] = topic_title
        tweet['name'] = self.converter.getName(status)
        tweet['username'] = self.converter.getUsername(status)
        tweet['to'] = self.converter.getTo(status)
        tweet['text'] = self.converter.getText(status)
        tweet['retweets'] = self.converter.getRetweets(status)
        tweet['favorites'] = self.converter.getFavorites(status)
        tweet['replies'] = self.converter.getReplies(status)
        tweet['permalink'] = self.converter.getPermalink(status)
        tweet['author_id'] = self.converter.getAuthorId(status)
        tweet['date'] = self.converter.getDate(status).__str__()
        tweet['formatted_date'] = self.converter.getFormattedDate(status)
        tweet['hashtags'] = self.converter.getHashtags(status)
        tweet['mentions'] = self.converter.getMentions(status)
        tweet['geo'] = self.converter.getGeo(status)
        tweet['urls'] = self.converter.getUrls(status)
        tweet['img_url'] = self.converter.getProfileImgUrl(status)
        emotion = self.converter.getEmotion(status)
        tweet['polarity'] = emotion.polarity
        tweet['subjectivity'] = emotion.subjectivity
        return tweet
