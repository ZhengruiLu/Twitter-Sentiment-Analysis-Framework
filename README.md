# Twitter's Sentiment
Social networks are a fascinating domains for applying concepts from data science and visualization. Not only are they sources of **big** "big data" (about 500 million tweets are sent on Twitter each _day_), but their status as personal communities means that they often can provide profound insights into how people think, feel, and interact. For example, researchers have shown that the "mood" of Twitter communication [reflects biological rhythms](http://www.nytimes.com/2011/09/30/science/30twitter.html) and can even be used to [predict the stock market](http://arxiv.org/pdf/1010.3003&embedded=true).

For this assignment, you will write a program to perform simple [sentiment analysis](https://en.wikipedia.org/wiki/Sentiment_analysis) of Twitter data---that is, determining the "attitude" of tweets (how "positive" or "negative") about a particular topic. You will apply this program to **real data** taken directly from Twitter, and use your analysis to consider basic questions about people's attitudes on social media.

- I want to emphasize that this assignment involves working with **real, unfiltered, unsanitized data** taken directly from the Twitter "firehose"--all public tweets made. _Tweets may include offensive, inappropriate, or triggering language or content._  As with the rest of the Internet, any given moment on Twitter can reveal both the peaks and valleys of human behavior. If you are concerned about this data or assignment in any way, please let us know.
    

### Objectives
By completing this challenge you will practice and master the following skills:

* Working with Python data structures: lists, dictionaries, and tuples
* Using Python loops and conditionals
* Defining re-usable functions that take in parameters and return data
* Programmatically processing, filtering, and organizing textual data
* Accessing a public data API

## Setup: Fork and Clone
As you will do for all assignments in this course, you should start by forking and cloning this repository to your local machine. Repositories will contain starter code (if any), as well as the `SUBMISSION.md` file you will need to complete.

For this assignment, the repo includes the start of a program `tweet_sentiments.py` which you will need to complete. The provided code provides a **command-line interface** that you will use to run your analysis program---your task will be to create the ___functions___ that the command-line interface calls to do work.

This command-line interface includes a number of ___subcommands___ (similar to how the `git` program contains subcommands like `add`, `commit`, and `push`. You can get help on the arguments for any subcommand (or just a list of options) with the `-h` command-line argument

```
python3 tweet_sentiments.py -h
```

This write-up will also be explicit about specify arguments for each task.

- Note that each of these commands will crash until you provide the appropriate function!

The repo also contains a number of data files. The `data/` folder has some sample Twitter data that you can test your program with. `sentiments_ucb.csv` and `AFINN-111.csv` are comma-separated list of "sentiment ratings" for common words (using different scales).

Finally, the repo contains a script `twitter_stream.py` that you'll be able to use to download your own Twitter data near the end of the assignment.


## Part 1. Sentiment Analysis
For the first part of this assignment, you will provide functions to analyze the sentiment of a short piece of text, like what would be found in a tweet. These functions will then be used to analyze the Twitter data in the next section.

* **IMPORTANT**: be very careful to name your functions ___exactly___ as specified in the spec, with the indicated parameters (in the indicated order!) The command-line interface is written to call those functions, and if they aren't correct your program will produce an error!

* There are lots of functions to implement for this assignment. I recommend you `add` and `commit` your code to git after you complete each one!


### 1A. Extract Words
Implement a function **`extract_words()`** that takes in a string of text as its single parameter and _returns_ a `list` of the words in that string.

- You should apply your newly-developed regular expression skills with Python's [regex module](https://docs.python.org/3.5/library/re.html) to easily find the delimiters ("breaks") between words. Watch out for apostrophes!

- You should also make sure that your list doesn't contain any "empty string" elements (e.g., that you've removed them).

You can test this function with

```
python3 tweet_sentiments.py extract_words "There're six words in this string."
```

which should produce an output:

```
["There're", 'six', 'words', 'in', 'this', 'string']
```
- Your function (and in fact all of your functions) should just _return_ a value, not print out the results! You are welcome to include print statements for testing, but be sure to remove them when you're done!


### 1B. Load the Sentiment File
Implement a function **`load_sentiments()`** that takes in as a parameter the name of a file containing word sentiment scores (e.g., `AFINN-111.txt`). The function should _return_ a `dictionary` whose keys are the words in and whose values are the numeric sentiment scores of those words.

- You can assume that the sentiment file contains _comma-separated values_; that is, each line contains a single word and its score, separated by a comma. Inspect the provided files for an example (note that `.csv` files are plain text, so you can open them in Sublime just as effectively as in Excel).

You can test this function with

```
python3 tweet_sentiments.py load_sentiments AFINN-111.csv 
```

which should produce an output that is a listing of the words following by their sentiments.

```
abandon -2.0
abandoned -2.0
...
```
The list is ordered alphabetically by the command-line system; your function does not need to "sort" your dictionary (and indeed, dictionaries are unordered by definition!)


### 1C. Get Sentiment of Text
Implement a function **`text_sentiment()`** (singular) that takes in two parameters: the text (a string) to analyze, and a dictionary of word sentiment values. The function should _return_ the sentiment of the text, defined as: _the sum of the sentiments of the words in the string_.

- This function will be _passed_ a sentiments dictionary produce by your `load_sentiments()` function. That function will be called by the included command-line parser; you do not need to call it yourself here.
    - This does mean that the `load_sentiments()` method must be working correctly for this function to work!

- A word that is not in the sentiments dictionary has a sentiment score of `0`.

You can test this function with

```
python3 tweet_sentiments.py sentiment -s AFINN-111.csv -t I prefer the rain to sunshine
```

which should have a sentiment of `2.0` (using the AFINN scores).

Try out the command with different phrases (ones that you feel would be "positive" and "negative") to see how the scoring works. 


## Part 2. Twitter Data
Now that you can calculate the sentiment of text, you can apply that to real Twitter data!

### 2A. Loading Tweets
For this assignment, you'll be loading Twitter data from a file, rather than directly from the live stream (this helps with testing and reproducibility).

Implement a function **`load_tweets()`** that takes in the name of a file containing tweets, and _returns_ a `list` of objects (dictionaries) representing those tweets.

These "tweet files" will be structured with _one tweet on each line_, with that tweet represented as a [JSON](https://en.wikipedia.org/wiki/JSON) formatted string (JSON format is very close to Python's dictionary syntax). You can open the example files in the `data/` folder to view this structure.

- You will likely notice a lot of non-English characters and words. Twitter is an international community and the data we're using will reflect that! Our analysis methods will be biased towards English-language speakers

    - **Important:** If you have problems with your command-line (e.g., Git Bash on Windows) not supporting [Unicode](https://en.wikipedia.org/wiki/Unicode) correctly and crashing, you can use the `tweet_sentiments-win.py` script file instead. This will encode the output so it doesn't crash while testing.

- This is real-world data and so will be messy! 

You will notice that each tweet contains [**a lot**](https://dev.twitter.com/overview/api/tweets) of information, including lots of details that we're not interested in. The dictionary your function returns should only include a subset of these fields. Specifically, you should include:

- **`created_at`**: when the tweet was posted
- **`user.screen_name`** (the `screen_name` value inside the `user` dictionary): who authored the tweet (attribution is important!) 
- **`text`** the content of the tweet; the part we most care about
- **`entities.hashtags[i].text`** (the `text` field from _each_ item in the `entries.hashtags` list). These are the [hashtags](https://en.wikipedia.org/wiki/Hashtag) that Twitter has extracted from the tweets (so you don't have to!)
- **`retweet_count`** how many times the tweet has been retweeted
- **`favorite_count`** how many times the tweet has been favorited

You won't be using all of these directly in your program, but you should still include them in your returned dictionary. You can include other information if you want, but I recommend against it as it makes things harder to read and debug.

Each tweet's data is encoded in `JSON` format, which is very close to a Python dictionary---and in fact, it's easy to convert between them using the [`json`](https://docs.python.org/3/library/json.html) module.

- You can use the `json.loads(json_string)` function, which takes in a JSON String and returns a Python dictionary of that String. 
- Remember to `import` the module to use its functions!

You can test this function with

```
python3 tweet_sentiments.py load_tweets data/dog.txt 
python tweet_sentiments_win.py load_tweets data/dog.txt 
```

which should produce an output that is each tweet as a dictionary (one per line), such as:

```
{'created_at': 'Thu Apr 21 16:03:39 +0000 2016', 'text': "It doesn't take long for a dog to win over a person's heart. The scene opens with a young boy's eyes glued to a... https://t.co/zjVLUk2afA", 'favorite_count': 0, 'hashtags': [], 'retweet_count': 0, 'user_name': 'sweetlaurakay'}
```
Note that the exact order of the fields might vary, since dictionaries are unordered!


### 2B. Tweet Popularity
After you've loaded the data, it's time to analyze it! Implement a function **`popularity()`** that takes in the name of a file containing tweets and _returns_ a `tuple` containing the average number of _retweets_ (in the first entry) and the average number of _favorites_ (in the second entry). This should give you a sense for how popular the data-set as a whole is, while letting you practice some basic accumulation.

- This method should _call_ the `load_tweets()` method you previously wrote---don't duplicate the logic to extract data from the tweet file!

- Remember that `tuples` can be declared using parentheses (e.g., `(1, 2)`)

You can test this function with

```
python3 tweet_sentiments.py popularity data/dog.txt
python tweet_sentiments_win.py popularity data/dog.txt 
```

which should print out your returned tuple:

```
(1178.39, 0.0)
```
(No one is favoriting the tweets in my dog data file it seems).


### 2C. Trending Hashtags
Implement a function called **`hashtag_counts()`** that takes in the name of a file containing tweets and _returns_ a `list` of tuples, where each tuple contains a hashtag in the data set and the number of times that hashtag was used (in that order). This list itself should be **ordered** by the frequency, so that most popular hashtags are at the top.

- Again, you should re-use your `load_tweets()` function here.

- It's useful to use a dictionary to count frequencies, even if you convert that data to a tuple later.

- Remember that tuples naturally sort (e.g., with the [`sorted()`](https://docs.python.org/3/library/functions.html#sorted) function) by the first value, then the second. So a neat trick is to take the list and "reverse" the tuple (swapping the first and second entries), then sort the list, then swap the entries back.

You can test this function with

```
python3 tweet_sentiments.py hashtag_counts data/dog.txt 
python tweet_sentiments_win.py hashtag_counts data/dog.txt 
```

which should print out your list of hashtags:

```
#dog : 5
#youtube : 2
#wanko : 2
#pet : 2
#inu : 2
```
(You should add the `#` in front of the hashtag). The sorting also needs to be done by you!


## Part 3. Twitter Sentiments
You've got sentiment analysis methods and twitter data, so it's time to combine the two!

### 3A. Tweet Sentiments
Implement a function **`tweet_sentiments()`** (plural) that takes in two parameters: the name of the tweet data file and the name of a sentiment data file (in that order). This function should _return_ a list of tweet objects (similar to your `load_tweets()` method, but with one difference: each tweet object should have an additional field (e.g., `sentiment`) that holds the sentiment of the tweet's text. This return value structure will allow you to re-use this function in the future (without requiring your program to process the entire tweet file repeatedly).

- This function should reuse your previously-written functions whenever possible. Don't repeat your work! In fact, this function will end up being pretty simply because you've already done most of the work.

You can test this function with

```
python3 tweet_sentiments.py sentiment -f data/dog.txt -s AFINN-111.csv
python tweet_sentiments_win.py sentiment -f data/dog.txt -s AFINN-111.csv
```

which should produce an output that is each tweet as a dictionary (one per line), such as:

```
{'sentiment': 4.0, 'created_at': 'Thu Apr 21 16:03:39 +0000 2016', 'user_name': 'sweetlaurakay', 'text': "It doesn't take long for a dog to win over a person's heart. The scene opens with a young boy's eyes glued to a... https://t.co/zjVLUk2afA", 'favorite_count': 0, 'retweet_count': 0, 'hashtags': []}
```
Again, the order of the fields may vary.


### 3B. Hashtag Sentiment
Now that you've calculated sentiments of tweets, we can start writing programs to ask and answer specific questions. For example: "Which hashtags are 'positive' and which are 'negative'?"

Implement a function **`hashtag_sentiments()`** that takes as parameters the name of a tweet data file and the name of a sentiment data file. This function should _return_ a `list` of tuples, where each tuple contains (in order) a hashtag in the data set and the sentiment of that hashtag, defined as: _the **average** sentiment of the tweets that contain that hashtag_. This list itself should be **ordered** by the sentiment, so that most positive hashtags are at the top.

- Calculating average on the go can be tricky, since you don't know how many tweets contain that hashtag ahead of time! Try to keep track of both the accumulated score and the number of tweets in a single loop; do not process the entire tweet file twice!

In addition, your function should take an [optional](http://www.diveintopython.net/power_of_introspection/optional_arguments.html) third parameter called **`query`**, representing a "search term". If the function is called with this parameter, then the returned list should _only_ contain hashtags that have the parameter's value _`in`_ them (e.g., if the query is `dog` then `dog` and `doggy` would both be returned).

- As always, be sure and call previously defined functions where-ever you can instead of re-writing code!

    - You may notice that this function does very similar work to the `hashtag_counts()` function. However, you won't be able to call that function without needing to either repeat code or causing the computer to load and process the tweet file twice (_think about why this is!_). Instead, if you want to re-use part of the `hashtag_counts()` method, you can "refactor" that code into an additional "helper" function that is called by both `hashtag_counts()` and `hashtag_sentiments()`.

You can test this function (with the optional query) with

```
python3 tweet_sentiments.py hashtag -f data/dog.txt -s AFINN-111.csv -q dog
```

which should produce a filtered set of hashtags:

```
#BulldogsAreBeautiful : 8.0
#doggydaycare : 2.0
#dog : 0.4
#DogCollar : 0.0
```
- It's fun to run this function with different sentiment files and see how there can be a range in what is considered a "positive" hashtag!


### 3C. Popular Sentiment
Let's answer one more question about general trends in twitter usage: "_based on a data set_, are positive or negative tweets more popular?"

Implement one last function **`popular_sentiment()`** that takes as parameters (again) the name of a tweet data file and the name of a sentiment data file. This function should _return_ the **correlation** (i.e., [Pearson's r](https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient)) between the sentiment of a tweet and the number of times that tweet was retweeted.

- This is a programming course and not a statistics course; there may be better measures to use to determine correlation given the data set and question we're asking. If we should be using a different measure, please let me know!

The math for calculating a Pearson's coefficient is not terribly complicated, but it's easy to make mistakes. A better solution is to use an existing statistical or scientific library. There are two incredibly popular libraries for Python: [SciPy](https://www.scipy.org/) and [NumPy](http://www.numpy.org/) (the existence of these libraries is part of why Python is so popular for data science!).

- These libraries aren't included with Python by default: if you want to be able to `import` them, you need to install them on your machine. Luckily, it's very easy to install a package for Python using the [`pip`](https://pip.pypa.io/en/stable/) command-line utility that comes with Python. For example:

    ```
    pip install scipy
    ```
    will download and install the SciPy library on your computer.
    
    - If you want to keep different versions of Python and packages organized, I recommend using [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), but that is not a requirement.

- Functions to calculate Pearson's coefficient are available in both [SciPy](http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.pearsonr.html) and [NumPy](http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.corrcoef.html) (I think the SciPy one is a bit more readable).

    - You'll need to `import` the package that the function is in. This includes the subpackage indicated by dots (e.g., `scipy.stats`).


You can test this function with

```
python3 tweet_sentiments.py correlation -f data/dog.txt -s AFINN-111.csv
```

which should print the correlation for you:

```
Correlation between popularity and sentiment: r=-0.0507906865784
```
This indicates that there is a _very, very slight_ correlation between positive tweets and retweets, but not enough to be anything close to significant.


## Part 4. Live Data
At this point you've finished writing your tweet sentiment analysis program! However, there's one more step: you've been testing against a small data set, but to really get interesting insights we need to go bigger. For this step, you should download a **large** number of tweets and then run your analysis program on them!

In order to download some Twitter data on your own, use the following steps:

1. Create a Twitter account if you do not already have one
2. Go to [https://apps.twitter.com/](https://apps.twitter.com/) and log in with your Twitter credentials
3. Click "Create New App"
4. Fill out the form and agree to the terms. You can put in a dummy website (e.g., `http://example.com` if you don't have one you want to use)
5. On the next page, click the "Keys and Access Tokens" tab along the top, then scroll all the way down until you see the section "Your Access Token". Click the "Create my access token" button. These tokens are used for [Oauth](https://dev.twitter.com/oauth/overview/faq) authentication (e.g., to allow your app to "sign in").
6. Open up the provided `twitter_stream.py` file. You should see four variables currently assigned placeholders:

    ```python
    # Your access information goes here
    CONSUMER_KEY = "<your key here>"
    CONSUMER_SECRET = "<your secret here>"
    ACCESS_TOKEN_KEY = "<your key here>"
    ACCESS_TOKEN_SECRET = "<your secret here>"
    ```

    Replace these strings (including the `< >`) with the values from your Twitter app page. Note that "Consumer Key" and "API Key" are synonyms).
7. Install the [TwitterAPI](https://github.com/geduldig/TwitterAPI) library (see the documentation for what command will install it!)
8. Run the program:

    ```
    python3 twitter_stream.py     
    ```
    You can redirect `>` the output to a file in order to save the results.

The program is currently set up to [stream data](https://dev.twitter.com/streaming/public
) from the live Twitter stream (the "firehose"). This will produce _a lot_ of data. In order to stop the program from streaming, hit **`Ctrl+C`**.

- You can also change the script so that it streams tweets about a particular topic, or that it fetches recent-ish [search](https://dev.twitter.com/rest/reference/get/search/tweets) results (rather than streaming them live).

Let the program stream data to a file for **3 to 10 minutes**. Note that you get about 10 megabytes of data---about 2000 tweets---every minute, so don't forget about this for too long!

Once you've downloaded some data, you should feed that into your sentiment analyzer! Calculate the sentiment of hashmaps, check for correlations between sentiment and popularity, and otherwise consider what we can learn from the program you wrote. 

To "turn in" your work from this section, you should do the following:

1. `add` and `commit` a _separate_ file containing **100** lines from your downloaded data file. The `head` and `tail` commands are useful for this.

    - **DO NOT COMMIT THE FULL DATA FILE!** It is way to big, and we don't want it!

    - Also, you should avoid committing the changes you made to the `twitter_stream.py` file. It's a **bad** idea to put your API Keys online (it's like posting your password on the Internet!), even if they are in a private repository.

2. Briefly answer the question in the `SUBMISSION.md` file about your findings.


## Submit Your Solution
Remember to `add`, `commit`, and `push` your script once it's finished!

In order to submit you assignment, you  need to both `push` your completed solution to your GitHub repository (the one in the cloud that you created by forking), **and** submit a link to your repository to [Canvas](https://canvas.uw.edu/) (so that we know where to find your work)!

Before you submit your assignment, double-check the following:

1. Confirm that your program is completed and works without errors. All of the commands included should be able to run without errors, producing the expected output. 
* Be sure and fill out the **`SUBMISSION.md`** included in the assignment directory, answering the questions.
* `commit` the final version of your work, and `push` your code to your GitHub repository.

Submit a a link to your GitHub repository via [this canvas page](https://canvas.uw.edu/courses/1041440/assignments/3208930).

The assignment is due on **Fri Apr 29 at 5:00 PM**.

### Grading Rubric
See the assignment page on Canvas for the grading rubric.

_Based on assignments by John DeNero, Aditi Muralidharan, et al., and Bill Howe._ 