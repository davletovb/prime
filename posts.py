import praw
import pandas as pd
import datetime as dt
import os
import re

reddit_client_id = os.environ['REDDIT_CLIENT_ID']
reddit_client_secret = os.environ['REDDIT_CLIENT_SECRET']
reddit_user_agent = 'REDDIT_USER_AGENT'


class RedditScraper:
    """
    A class that defines a Reddit scraper using the praw library.
    """

    def __init__(self):

        # create reddit instance
        # get reddit credentials from environment variables
        self.reddit = praw.Reddit(client_id=reddit_client_id,
                                  client_secret=reddit_client_secret, user_agent=reddit_user_agent)

    def download_posts(self, subreddit, limit=100):
        """
        Downloads and saves the specified number of posts and comments from the subreddit.
        """
        subreddit = self.reddit.subreddit(subreddit)
        print("Getting {} number of posts from /r/{}".format(limit, subreddit))
        # get posts and comments
        posts = []
        for post in subreddit.hot(limit=limit):
            posts.append([post.title, post.selftext, post.created,
                         post.score, post.subreddit, post.id, post.num_comments])
            post.comments.replace_more(limit=0)
            for comment in post.comments:
                try:
                    comment.num_comments = len(comment.replies)
                except:
                    comment.num_comments = 0

                posts.append([post.title, comment.body, comment.created,
                             comment.score, comment.subreddit, comment.id, comment.num_comments])

        # create dataframe
        posts = pd.DataFrame(
            posts, columns=['title', 'body', 'created', 'score', 'subreddit', 'id', 'comments'])

        # convert timestamp to datetime
        def get_date(created):
            return dt.datetime.fromtimestamp(created)

        posts["created"] = posts["created"].apply(get_date)

        # save to csv
        posts.to_csv('data/reddit_'+str(posts['subreddit']
                     [0])+'.csv', index=False, escapechar='\\')

        return posts

    def clean_posts(self, filename):
        """
        Cleans the posts and saves them as a text file.
        """
        # get the file and read it into a dataframe
        df = pd.read_csv(filename)
        subreddit = df['subreddit'][0]

        # drop rows with missing body text
        df.dropna(subset=['body'], inplace=True)

        # remove urls
        df['body'] = df['body'].apply(lambda x: re.sub(r'http\S+', '', x))

        # drop all the columns except title and body
        df = df[['title', 'body']]

        # save as a text file, no structure
        df.to_csv('data/documents/reddit_'+str(subreddit) +
                  '.txt', index=False, header=False)

        with open('data/documents/reddit_'+str(subreddit)+'.txt', 'r') as f:
            lines = f.readlines()

        return lines
