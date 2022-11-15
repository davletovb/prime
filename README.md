# About
Prime is a question answering system for products using the haystack framework. It allows you to quickly and easily find information about products, including comparisons and pros/cons. You can also use Prime to read summarized reviews and find product ratings from Reddit and Wirecutter reviews.

# Python version
Works with python 3.9 and 3.10, python 3.11 doesn't work yet.

# Requirements
To install these requirements, first run this:

pip install -r requirements.txt

After installing everything successfully with no errors or warnings raised, it will download models from huggingface for the first run. Consecutive model queries should work faster from the local cache.

# Data
"Data" directory has example posts and comments taken directly off Reddit plus reviews scraped from Wirecutter blog.
