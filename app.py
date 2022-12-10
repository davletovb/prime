from forms import QuestionForm, RedditForm, UploadForm
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, session
from query import QAPipeline
from posts import RedditScraper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    question_form = QuestionForm()
    reddit_form = RedditForm()
    upload_form = UploadForm()
    return render_template('index.html', question_form=question_form, reddit_form=reddit_form, upload_form=upload_form)


@app.route('/answer', methods=['POST'])
def answer():
    question = request.form['question']
    query = QAPipeline()
    answer = query.answer(question)
    return render_template('answer.html', question=question, answer=answer)


@app.route('/reddit', methods=['POST'])
def reddit():
    subreddit = request.form['subreddit']
    session['subreddit'] = subreddit
    limit = int(request.form['limit'])
    scraper = RedditScraper()
    reddit_posts = scraper.download_posts(subreddit, limit)
    return render_template('reddit.html', subreddit=subreddit, limit=limit, reddit_posts=reddit_posts)


@app.route('/upload', methods=['POST'])
def upload():
    import pandas as pd
    file = request.files['file']
    df = pd.read_csv(file.filename)
    session['subreddit'] = df['subreddit'][0]
    return render_template('upload.html', subreddit=session['subreddit'], num_posts=len(df), csv_file=file.filename, posts=df)


@app.route('/clean', methods=['POST'])
def clean():
    subreddit = session['subreddit']
    csv_file = 'reddit_'+subreddit+'.csv'
    scraper = RedditScraper()
    cleaned_text = scraper.clean_posts(csv_file)
    txt_file = 'reddit_'+subreddit+'.txt'
    return render_template('clean.html', txt_file=txt_file, cleaned_text=cleaned_text)


if __name__ == '__main__':
    app.run(host='localhost', port=9000, debug=True)
