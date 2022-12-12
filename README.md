# Prime

## Overview

Prime is a question answering system for products that uses natural language processing and machine learning techniques to quickly and easily find information about products. By using the Haystack framework, Prime is able to analyze large amounts of product-related data and provide accurate answers to questions about products, including comparisons and pros/cons. Additionally, Prime can access reviews and ratings from sources such as Reddit and Wirecutter to provide users with more detailed information about the products they are interested in. Overall, Prime is a tool for quickly and easily finding information about products.

## Applications

* Quickly and easily find information about products: Prime allows users to ask questions about products and receive accurate, detailed answers in a matter of seconds. This makes it easy for users to find the information they need about a wide range of products, including comparisons and pros/cons.
* Compare products: Prime's ability to access and analyze large amounts of product-related data makes it a useful tool for comparing different products. Users can ask questions such as "What is the difference between Product A and Product B?" and receive detailed answers that highlight the key features and differences between the two products.
* Read summarized reviews and ratings: Prime can access reviews and ratings from sources such as Reddit and Wirecutter and provide users with a summary of the most important information. This can help users quickly and easily get a sense of the general sentiment around a product and make more informed decisions about whether to buy it.

## Usage

* Clone Repo:
```
git clone https://github.com/davletovb/prime.git
```

* Setup a virtual environment: 
```
virtualenv .virtualenv/prime
```

* Activate virtual environment:
```
source .virtualenv/prime
```

* To install these requirements, first run this:
```
pip install -r requirements.txt
```

* Set environment variables:

```
export SECRET_KEY="SECRET_KEY"
export REDDIT_CLIENT_ID="REDDIT_CLIENT_ID"
export REDDIT_CLIENT_SECRET="REDDIT_CLIENT_SECRET"
```

The client id and secret for Reddit can be obtained by filling a form at: https://old.reddit.com/prefs/apps

* After installing everything successfully with no errors or warnings raised, it will download models from huggingface for the first run. Consecutive model queries should work faster from the local cache.

* If Docker is installed the app will try to launch Elasticsearch. Otherwise you can just run Elasticsearch separately and change the "host:port" parameters for it.

## Datasets
* "Data" directory has example posts and comments taken directly off Reddit plus reviews scraped from Wirecutter blog.

## Milestones
* Haystack framework implemented, with a model that can generate long form answers to questions.
* Building a web application where users can ask questions and get answers about the products.
