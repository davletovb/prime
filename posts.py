import praw
import pandas as pd
import datetime as dt
import os
import re


def download_reddit_posts(subreddit, limit=100):

    # create reddit instance
    # get reddit credentials from environment variables
    reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                         client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                         user_agent="REDDIT_USER_AGENT")

    subreddit = reddit.subreddit(subreddit)
    print("Getting {} number of posts from /r/{}".format(limit, subreddit))
    # get posts and comments
    posts = []
    for post in subreddit.hot(limit=limit):
        posts.append([post.title, post.selftext, post.created,
                     post.score, post.subreddit, post.id, post.num_comments])
        post.comments.replace_more(limit=0)
        for comment in post.comments:
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
    posts.to_csv('reddit_'+str(posts['subreddit']
                 [0])+'.csv', index=False, escapechar='\\')

    return posts


def clean_posts(filename):
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
    df.to_csv('data/article_txt_got/reddit_'+str(subreddit) +
              '.txt', index=False, header=False)

    with open('data/article_txt_got/reddit_'+str(subreddit)+'.txt', 'r') as f:
        lines = f.readlines()

    return lines
