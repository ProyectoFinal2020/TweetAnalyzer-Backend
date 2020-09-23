from ...models.tweetAndScore import TweetAndScore


def mapToTweetAndScore(scores, tweets, preprocessed_documents):
    tweetsAndScore = []
    for i in range(len(tweets)):
        tweetsAndScore.append(TweetAndScore(
            tweet=tweets[i],
            tweetWithoutStopwords=preprocessed_documents[i],
            score=scores[i]))
    return tweetsAndScore
