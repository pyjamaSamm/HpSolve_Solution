import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer
import ssl
from textblob import TextBlob
from flask import Flask, jsonify, request, render_template
import networkx as nx
import tweepy

# ------------------------------data collection--------------------------------------

# get HP related posts from twitter using twitter API


# enter your Twitter API credentials
consumer_key = "YOUR CONSUMER KEY"
consumer_secret_key = "YOUR CONSUMER SECRET KEY"
access_token = "YOUR ACCESS TOKEN"
access_token_secret = "YOUR ACCESS SECRET TOKEN"

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret_key)
api = tweepy.Client(auth)

# returns 10 posts on HP related posts
tweets = api.search_all_tweets(query="HP", lang="en", count=10)
# ------------------------------end of data collection--------------------------------------

# stores the tweets and its corresponding sentiments
tweetList = []
sentimentList = []

class tweetsClass:
    def __init__(self, id, tweet, product_type, product_model):
        self.id = id
        self.tweet = tweet
        self.product_type = product_type # for knowledge graph
        self.product_model = product_model # for knowledge graph

class sentimentClass:
    def __init__(self, id, sentiment):
        self.id = id
        self.sentiment = sentiment


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')

# dummy posts
tweets = [
    "HP laptop is amazing!",
    "HP is not working properly.",
    "HP printer is having Wi-Fi issues.",
    "HP products are known for their best quality and reliability.",
    "The HP PC crashed unexpectedly.",
    "Just bought the new HP Spectre x360, and it's absolutely amazing!",
    "Having some wifi issues with my HP Envy laptop. Need some help troubleshooting.",
    "The HP EliteBook is perfect for my business needs. Highly recommended!",
    "Experiencing Wi-Fi connectivity problems with my HP LaserJet printer. Any solutions?",
    "Impressed with the performance of my new HP ZBook workstation! It's a powerhouse!",
    "Just ordered the HP DeskJet Ink Advantage printer. Can't wait to try it out!",
    "The HP Omen gaming laptop exceeded my expectations. It handles graphics-intensive games flawlessly.",
    "Thinking of upgrading my old HP Pavilion desktop to the latest model. Any recommendations?"
]

englishStopwords = stopwords.words("english")
stemmer = PorterStemmer()
tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)

processedTweets = []
ID_count = 0

# Knowledge Graph
graph = nx.Graph()

# ---------------------------------Data processing--------------------------------------
for tweet in tweets:
    # Extract product type and model from tweet
    product_type = re.findall(r"(?i)(laptop|printer|pc|product|computer)", tweet)
    product_model = re.findall(r"(?i)(\b[A-Za-z0-9]+\b)", tweet)

    tweetList.append(tweetsClass(ID_count, tweet, product_type, product_model))
    ID_count += 1

    tweet = re.sub(r'^RT[\s]+', '', tweet)  # remove retweet
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)  # remove URL
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)  # remove tags/mentions
    tweet = re.sub(r'[^a-zA-Z0-9\s]+', '', tweet)  # remove special characters

    # Tokenize the tweet
    tokens = tokenizer.tokenize(tweet)

    clean_tokens = [] # for storing after removing stopwords and stemming the words
    for token in tokens:
        if token not in englishStopwords:
            stem_token = stemmer.stem(token) # perform stemming and reduce the words to its roots
            clean_tokens.append(stem_token)

    processedTweet = ' '.join(clean_tokens)
    processedTweets.append(processedTweet)


    # ---------------------------knowledge graph--------------------------------

    # Add product type and model as nodes to the knowledge graph
    if product_type:
        graph.add_node(product_type[0])
    if product_model:
        for model in product_model:
            graph.add_node(model)

    # ---------------------------knowledge graph--------------------------------

# for tweet in processedTweets:
#     print(tweet)

# ---------------------------------Data processing ends--------------------------------------

ID_count = 0




# ---------------------------------Text Classification---------------------------
# to improve sentiment analysis
negative_sentiments = {"not working", "has issues", "crashed", "crashing"}
positive_sentiments = {"amazing", "best", "good"}

for tweet, processedTweet in zip(tweetList, processedTweets):
    blob = TextBlob(tweet.tweet) # textBlob is used to 
    sentiment = blob.sentiment

    polarity = sentiment.polarity # numeric value of the sentiment is assigned

    if polarity > 0:
        sentimentType = 'Positive'
    elif polarity < 0:
        sentimentType = 'Negative'
    else:
        if any(string.lower() in tweet.tweet.lower() for string in negative_sentiments):
            sentimentType = 'Negative'
        elif any(string.lower() in tweet.tweet.lower() for string in positive_sentiments):
            sentimentType = 'Positive'
        else:
            sentimentType = 'Neutral'

    sentimentList.append(sentimentClass(ID_count, sentimentType))
    ID_count += 1


    # ---------------------------knowledge graph--------------------------------

    # Add edges between product type/model and sentiment in the knowledge graph
    if tweet.product_type:
        for product_type in tweet.product_type:
            graph.add_edge(product_type, sentimentType)
    if tweet.product_model:
        for product_model in tweet.product_model:
            graph.add_edge(product_model, sentimentType)

    # ---------------------------knowledge graph--------------------------------


# print("\n\nTweet list created\n")
# ---------------------------------Text Classification ends---------------------------





# ---------------------------------Web API Development---------------------------------

app = Flask(__name__, template_folder='templates')

sample_data = {
    'tweets': [],
    'sentiments': []
}

for tweet, sentiment in zip(tweetList, sentimentList):
    sample_data['tweets'].append({'id': tweet.id, 'text': tweet.tweet})
    sample_data['sentiments'].append({'id': sentiment.id, 'sentiment': sentiment.sentiment})

@app.route("/", methods=['GET'])
def home():
    return render_template('form.html')

@app.route("/tweets", methods=['GET'])
def get_tweets():
    return jsonify(sample_data['tweets'])

@app.route("/sentiments", methods=['GET'])
def get_sentiments():
    return jsonify(sample_data['sentiments'])

@app.route("/query", methods=['POST'])
def query_posts():
    query = request.form['query']  # Get the query from the user's input
    relevant_posts = []

    query_blob = TextBlob(query)
    query_sentiment = query_blob.sentiment
    query_polarity = query_sentiment.polarity

    if query_polarity > 0:
        query_sentiment_type = 'Positive'
    elif query_polarity < 0:
        query_sentiment_type = 'Negative'
    else:
        if any(string.lower() in query.lower() for string in negative_sentiments):
            query_sentiment_type = 'Negative'
        elif any(string.lower() in query.lower() for string in positive_sentiments):
            query_sentiment_type = 'Positive'
        else:
            query_sentiment_type = 'Neutral'

    # Extract product type and model from the query
    product_type_query = re.findall(r"(?i)(laptop|printer|pc)", query)
    product_model_query = re.findall(r"(?i)(\b[A-Za-z0-9]+\b)", query)

    # Expand the query using the knowledge graph
    for tweet in tweetList:
        if (product_type_query and tweet.product_type and any(
                pt.lower() in tweet.product_type for pt in product_type_query)):
            relevant_posts.append(tweet.tweet)
        elif (product_model_query and tweet.product_model and any(
                pm.lower() in tweet.product_model for pm in product_model_query)):
            relevant_posts.append(tweet.tweet)
        elif sentiment.sentiment == query_sentiment_type:
            relevant_posts.append(tweet.tweet)

    # Expand the query using the knowledge graph
    if product_type_query or product_model_query:
        expanded_query = set(product_type_query + product_model_query)
        related_nodes = set()
        for node in expanded_query:
            if node in graph.nodes:
                related_nodes.update(nx.neighbors(graph, node))
        related_posts = []
        for tweet in tweetList:
            if any(node in tweet.tweet for node in related_nodes):
                related_posts.append(tweet.tweet)
        relevant_posts.extend(related_posts)

    # Return the relevant posts as a response
    if relevant_posts:
        bullet_relevant_posts = "<h2>"+query+"</h2>"
        bullet_relevant_posts += "<ul>"
        bullet_relevant_posts += "".join([f"<li>{post}</li>" for post in relevant_posts])
        bullet_relevant_posts += "</ul>"
        return bullet_relevant_posts
    else:
        return "No posts found for the given query."

if __name__ == '__main__':
    app.run()

# ---------------------------------Web API Development end---------------------------------
