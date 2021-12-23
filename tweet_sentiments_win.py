# Your functions go here!
# 1A
import re

def extract_words(text):
    pat = '[a-zA-Z]+'
    res = re.findall(pat,text)
    return [s.lower() for s in res]

# test = "There're 899324%8* &^&^& six words in      this string."
# extract_words(test)

# 1B
import csv

def load_sentiments(csvFile):

  f = open(csvFile, 'r')
  reader = csv.reader(f)
  result = {}

  for row in reader:
    result[row[0]] = float(row[1])

  return result

# 1C
def text_sentiment(text, sentimentDic):
  # use 1A to divide string into words
  # use 1B's dict to get value(score) of every word; 
  # sum all the scores
  wordsList = extract_words(text)

  sumScores = 0

  for word in wordsList:
    if word in sentimentDic:

        sumScores = sumScores + sentimentDic.get(word) 

  return sumScores

# 2A
import json 

def load_tweets(fileName):
  resultList = []
  newDict = {}

  with open(fileName) as txtData:
    lines = txtData.readlines()
    for line in lines:
      line_dict = json.loads(line)

      new_dict = {key: line_dict[key] for key in ['created_at', 'text', 'retweet_count', 'favorite_count']}

      new_dict['text'] = new_dict['text'].lower()
      new_dict['user.screen_name'] = line_dict.get('user').get('screen_name')

      new_dict['entities.hashtags[i].text'] = []
      hashtagsList = line_dict.get('entities').get('hashtags')
      for hashtagDict in hashtagsList:
          new_dict['entities.hashtags[i].text'].append(hashtagDict.get('text'))

      resultList.append(new_dict)
 
  return resultList

# 2B
def popularity(fileName):
  filelist = load_tweets(fileName)

  sumRetweets = 0
  countRetweets = 0
  sumFavorite = 0
  countFavorite = 0

  for tweetdict in filelist:
    # find retweets number
    # add it into sum
    sumRetweets = sumRetweets + tweetdict.get('retweet_count')
    countRetweets = countRetweets + 1
    # find favorites number
    # add it into its sum
    sumFavorite = sumFavorite + tweetdict.get('favorite_count')
    countFavorite = countFavorite + 1

  # calculate the average of retweets and fav, add them into tuple
  aveRetweets = float(sumRetweets / countRetweets)
  aveFavorite = float(sumFavorite / countFavorite)
  return tuple((aveRetweets, aveFavorite))     


# 2C. Trending Hashtags
def hashtag_counts(fileName):
  fileList = load_tweets(fileName)
  resDict = {}

# find hashtag as key, count times as value, sort by value
  for tweetDict in fileList:
    hashtagsList = tweetDict.get('entities.hashtags[i].text')
    hashtagsSet = set(hashtagsList)
    
    for hashtag in hashtagsSet:
        hashtag = '#' + hashtag

        if hashtag in resDict:
          resDict[hashtag] = resDict[hashtag] + 1
        else:
          resDict[hashtag] = 1

# transfer dict into tuple
  resTupleList = sorted(resDict.items(), key = lambda x : x[1], reverse = True)

  return resTupleList

# 3A
def tweet_sentiments(tweetDataFileName, SentimentDataFileName):
  # return_ a list of tweet objects
  # each tweet object should have an additional field ('sentiment')

  # use 2A load_tweets() produce a list of dicts
  # every dicts in this list should add one key: 'sentiment'
  # calculate the value of 'sentiment' by 1C text_sentiment()
  tweetsList = load_tweets(tweetDataFileName)
  sentimentDict = load_sentiments(SentimentDataFileName)

  for tweetDict in tweetsList:
    tweetDict['sentiment'] = text_sentiment(tweetDict['text'], sentimentDict)

  return tweetsList  

# 3B
# takes as parameters the name of a tweet data file and the name of a sentiment data file
# return_ a `list` of tuples, where each tuple contains (in order) a hashtag in the data set 
# and the sentiment of that hashtag, defined as: _the **average** sentiment of the tweets that contain that hashtag_.
# This list itself should be **ordered** by the sentiment, so that most positive hashtags are at the top.

# Try to keep track of both the accumulated score and the number of tweets in a single loop
def hashtag_sentiments(tweetDataFileName, SentimentDataFileName, query):

  # hashtag_counts(): returns_ a `list` of tuples, where each tuple contains a hashtag in the data set and the number of times that hashtag was used (in that order)
  # sentiment: the **average** sentiment of the tweets that contain that hashtag_
  # Try to keep track of both the accumulated score and the number of tweets in a single loop
  # if this text contains the target hashtag, sum += tweet's sentiment, cnt += 1
  # average sentiments = sum / count

  tweetsList = tweet_sentiments(tweetDataFileName, SentimentDataFileName)
  hashtagFrequencyDict = {}
  totalSentimentDict = {}
  resDict = {}
  resQueryDict = {}

# find hashtag as key, count times as value, sort by value
  for tweetDict in tweetsList:
    # get hashtags
    hashtagsList = tweetDict.get('entities.hashtags[i].text')
    hashtagsSet = set(hashtagsList)

    #calculate the hashtag's frequency
    for hashtag in hashtagsSet:
        hashtag = '#' + hashtag

        if hashtag in hashtagFrequencyDict:
          hashtagFrequencyDict[hashtag] = hashtagFrequencyDict[hashtag] + 1
          totalSentimentDict[hashtag] = totalSentimentDict[hashtag] + tweetDict.get('sentiment')
        else:
          hashtagFrequencyDict[hashtag] = 1
          totalSentimentDict[hashtag] = tweetDict.get('sentiment')

  # third parameter called **`query`**, representing a "search term".
  # If the function is called with this parameter, then the returned list should _only_ contain hashtags that have the parameter's value _`in`_ them
  # e.g., if the query is `dog` then `dog` and `doggy` would both be returned
  for hashtag in totalSentimentDict:
    if re.findall(query, hashtag.lower()):
        resDict[hashtag] = totalSentimentDict[hashtag] / hashtagFrequencyDict[hashtag]
        
  # transfer dict into tuple list
  resTupleList = sorted(resDict.items(), key = lambda x : x[1], reverse = True)

  return resTupleList  


# 3C. Popular Sentiment

# return_ the **correlation** between 
# the sentiment of a tweet and 
# the number of times that tweet was retweeted.

import numpy as np

def popular_sentiment(tweetDataFileName, SentimentDataFileName) :
  tweetsList = tweet_sentiments(tweetDataFileName, SentimentDataFileName)

  sentimentList = []
  retweetedNumList = []
  # x - get every sentiment number, and save into list
  # y - get every retweets number, and save into list
  for tweetDict in tweetsList:
    sentimentList.append(tweetDict.get('sentiment'))
    retweetedNumList.append(tweetDict.get('retweet_count'))
  
  # corrcoef(x, y)
  x = np.array(sentimentList)
  y = np.array(retweetedNumList)

  return np.corrcoef(x, y)

# result:
# Correlation between popularity and sentiment: r=[[ 1.         -0.04218625]
# [-0.04218625  1.        ]]

####################################
## DO NOT EDIT BELOW THIS POINT!! ##
## #################################
# Run the method specified by the command-line
if __name__ == '__main__':
    # for parsing and friendly command-line error messages
    import argparse
    parser = argparse.ArgumentParser(description="Analyze Tweets")
    subparsers = parser.add_subparsers(description="commands", dest='cmd')
    subparsers.add_parser(
        'load_tweets', help="load tweets from file").add_argument('filename')
    subparsers.add_parser(
        'popularity', help="show average popularity of tweet file").add_argument('filename')
    subparsers.add_parser('extract_words', help="show list of words from text").add_argument(
        dest='text', nargs='+')
    subparsers.add_parser(
        'load_sentiments', help="load word sentiment file").add_argument('filename')

    sentiment_parser = subparsers.add_parser(
        'sentiment', help="show sentiment of data. Must include either -f (file) or -t (text) flags.")
    sentiment_parser.add_argument(
        '-f', help="tweets file to analyze", dest='tweets')
    sentiment_parser.add_argument(
        '-t', help="text to analyze", dest='text', nargs='+')
    sentiment_parser.add_argument(
        '-s', help="sentiment file", dest="sentiments", required=True)

    subparsers.add_parser(
        'hashtag_counts', help="show frequency of hashtags in tweet file").add_argument('filename')

    hashtag_parser = subparsers.add_parser(
        'hashtag', help="show sentiment of hashtags.")
    hashtag_parser.add_argument(
        '-f', help="tweets file to analyze", dest='tweets', required=True)
    hashtag_parser.add_argument(
        '-s', help="sentiment file", dest="sentiments", required=True)
    hashtag_parser.add_argument(
        '-q', help="hashtag to analyze", dest="query", default=None)

    correlation_parser = subparsers.add_parser(
        'correlation', help="show correlation between popularity and sentiment of tweets")
    correlation_parser.add_argument(
        '-f', help="tweets file to analyze", dest='tweets', required=True)
    correlation_parser.add_argument(
        '-s', help="sentiment file", dest="sentiments", required=True)

    args = parser.parse_args()

    try:
        if args.text:
            args.text = ' '.join(args.text)  # combine text args
    except:
        pass

    # print(args) #for debugging

    # call function based on command given
    if args.cmd == 'load_tweets':
        tweets = load_tweets(args.filename)
        for tweet in tweets:
            print(str(tweet).encode('utf8'))

    elif args.cmd == 'popularity':
        print(popularity(args.filename))

    elif args.cmd == 'hashtag_counts':
        for key, value in hashtag_counts(args.filename):
            print(str(key).encode('utf8'), ":", value)

    elif args.cmd == 'extract_words':
        print(extract_words(args.text))

    elif args.cmd == 'load_sentiments':
        for key, value in sorted(load_sentiments(args.filename).items()):
            print(key, value)

    elif args.cmd == 'sentiment':
        if args.tweets == None:  # no file, do text
            sentiment = text_sentiment(
                args.text, load_sentiments(args.sentiments))
            print('"'+args.text+'":', sentiment)
        elif args.text == None:  # no text, do file
            rated_tweets = tweet_sentiments(args.tweets, args.sentiments)
            for tweet in rated_tweets:
                print(str(tweet).encode('utf8'))
        else:
            print(
                "Must include -f (tweet filename) or -t (text) flags to calculate sentiment.")

    elif args.cmd == 'hashtag':
        if(args.query == None):  # split to test optional param
            rated_tags = hashtag_sentiments(args.tweets, args.sentiments)
        else:
            rated_tags = hashtag_sentiments(
                args.tweets, args.sentiments, args.query)
        for key, value in rated_tags:
            print(str(key).encode('utf8'), ":", value)

    elif args.cmd == 'correlation':
        print("Correlation between popularity and sentiment: r=" +
              str(popular_sentiment(args.tweets, args.sentiments)))
