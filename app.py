import posts
import query
from flask import Flask, request, session

# run a Flask app to get the subreddit name and number of posts to scrape from the user\
app = Flask(__name__)
app.secret_key = 'super secret key'


# get subreddit name and number of posts to scrape
@app.route('/', methods=['GET', 'POST'])
def index():
    # ask user for subreddit name and number of posts to scrape from the user in a html form
    index_html = '''
    <html>
    <body>
    <h1>Reddit Question Answering</h1>
    <form action="/answer" method="post">
    <p><input type="text" name="question" size="100" />
    <input type="submit" value="Ask" /></p>
    </form>
    <h1>Get Reddit Posts</h1>
    <form action="/get_reddit" method="post">
    <label for="subreddit">Subreddit Name:</label><br>
    <input type="text" id="subreddit" name="subreddit" value="subreddit"><br>
    <label for="limit">Number of Posts to Scrape:</label><br>
    <input type="text" id="limit" name="limit" value="100"><br><br>
    <input type="submit" value="Download">
    </form>
    <p> 
        <strong>Upload a csv file: </strong> <br>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" />
            <input type="submit" value="Upload" />
        </form>
    </p>
    </body>
    </html>
    '''
    return index_html


# get the answer from the model
@app.route('/answer', methods=['POST'])
def answer():
    # get the question from the user
    question = request.form['question']

    # get the answer from the model
    answer = query.answer(question)

    # return the answer in a html format
    return '''
    <html>
    <body>
    <h1>Reddit Question Answering</h1>
    <form action="/answer" method="post">
    <p><input type="text" name="question" size="100"/>
    <input type="submit" value="Ask" /></p>
    </form>
    <p> 
    <form action="/" method="post">
    <input type="submit" value="Back">
    </form>
    </p>
    <h1>Answer: </h1>
    <p>{}</p>
    </body>
    </html>
    '''.format(answer)


# get the data from subreddit and save to csv
@app.route('/get_reddit', methods=['POST'])
def get_reddit():
    # get subreddit name and number of posts to scrape from the user
    subreddit = request.form['subreddit']
    session['subreddit'] = subreddit
    limit = int(request.form['limit'])
    # run get_reddit function with the subreddit name and number of posts to scrape
    reddit_posts = posts.download_reddit_posts(subreddit, limit)
    # return the output of get_reddit function
    posts_html = '''
    <html>
    <body>
    <h1>Reddit Posts</h1>
    <p>Subreddit: {}</p>
    <p>Number of Posts: {}</p>
    <p>CSV File: <a href="reddit_{}.csv">reddit_{}.csv</a></p>
    <p>
    <form action="/clean" method="post">
    <input type="submit" value="Clean">
    </form>
    <form action="/" method="post">
    <input type="submit" value="Back">
    </form>
    </p>
    <p>Posts:</p>
    {}
    </body>
    </html>
    '''.format(subreddit, limit, subreddit, subreddit, reddit_posts.to_html())
    return posts_html


# upload a csv file to clean
@app.route('/upload', methods=['POST'])
def upload():
    import pandas as pd
    # get the file from the user
    file = request.files['file']
    # add the csv file to dataframe
    df = pd.read_csv(file.filename)
    session['subreddit'] = df['subreddit'][0]
    # return the output of prepare_data function
    posts_html = '''
    <html>
    <body>
    <h1>Reddit Posts</h1>
    <p>Subreddit: {}</p>
    <p>Number of Posts: {}</p>
    <p>CSV File: <a href="reddit_{}.csv">reddit_{}.csv</a></p>
    <p>
    <form action="/clean" method="post">
    <input type="submit" value="Clean">
    </form>
    <form action="/" method="post">
    <input type="submit" value="Back">
    </form>
    </p>
    <p>Posts:</p>
    {}
    </body>
    </html>
    '''.format(df['subreddit'][0], len(df), df['subreddit'][0], df['subreddit'][0], df.to_html())
    return posts_html


# clean the data
@app.route('/clean', methods=['POST'])
def clean():
    # get the csv file name
    subreddit = session['subreddit']
    csv_file = 'reddit_'+subreddit+'.csv'
    # run the clean function with the csv file name
    cleaned_text = posts.clean_posts(csv_file)
    txt_file = 'reddit_'+subreddit+'.txt'
    # return the output of clean function
    cleaned_html = '''
    <html>
    <body>
    <h1>Cleaned TXT File</h1>
    <p>CSV File: <a href="{}">{}</a></p>
    <p>
    <form action="/" method="post">
    <input type="submit" value="Back">
    </form>
    </p>
    <p>Posts:</p>
    {}
    </body>
    </html>
    '''.format(txt_file, txt_file, cleaned_text)
    return cleaned_html


if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)
