# Posse 


## Description

A blog post webapp that analyses a users sentiment towards their discussed topics and allows other users to interact through a poll range of how much they agree with the post. It then provides users with analytics on that post and how the average user feels about that post. Users can also see how might other users interact with other posts.

Through sentiment analysis, any post users post get graded based on how the API analyses their text structure. The text analysis also provides us with the topics being discussed in each post. This allows us to take note of how this user may feel about this particular topic in that given post.

Users can also directly respond to posts via their own post to provide a greater emphasis on their thoughts about that particular post. If they feel comments may be more beneficial, that is an option as well. This direct response, can be found on the regular home page indicated with a response arrow, which users can interact with to directly take them to the post being responded to.

If a user is further intrigued by a post, their is a 'more on this' option when viewing the full posts. This 'more' section shows other posts that may have mentioned the link, the post, or the topic that that post is tied to. This is so that users can explore what others may have to say about those posts' contents.

Posts that have garnered a substantial amount of interactions (poll responses + comments) are considered relevant posts. These relevant posts are then linked to other posts like it that share the same topics. These posts are then connected together and are presented in the homepage as 'joint-posts' as long as they are completely of opposite sentiments. This is so that posts that are clearly being discussed are not stand alone and the other side of the argument is readily available. The goal is that both sides of an argument, no matter the topic, is deserving of being heard. It is in hopes of having a more open and clearer view of social media.

## Usage

MEANINGCLOUD API KEY is needed for main function. A key is provided but calls are limited.

#### app/models.py

```python
MEANINGCLOUD_KEY = 'key'
```

Reminder:

To create virtualenv:

>python3 -m venv venv

Activate venv:

>source venv/bin/activate

Install requirements.txt:

>pip install -r requirements.txt

### Start App
> To start app, a SECRET_KEY is needed.
#### Command line
```bash
SECRET_KEY='YourKeyHere' flask run
```

### Run Tests
>Tests via Pytest

##### Whole Test
```bash
python -m pytest -rP tests
```

##### Unit Test
> Tests models class and its functions
```bash
python -m pytest -rP tests/unit
```
##### Functional Test
> Tests all app routes
```bash
python -m pytest -rP tests/functional
```

## API used:

### MeaningCloud (Sentiment Analysis):
https://www.meaningcloud.com/

100 requests / month


### LinkPreview (Link Preview Generator):
https://api.linkpreview.net/

100 requests / day

## Project Status

Key features of project are complete. UI needs more development and some features are planned but are not implemented. 

### Things not implemented but would want to work on later:

1. Follow system; fully understand how it works just did not thing it was an important function to do immediately.

2. Search bar; Allows searches of topics, users, etc.

3. Filter based on topics; View different posts based on topics. There are buttons on each user profile that shows their last discussed topics and that would be a great place to start.

## Tech Stack:

Python, HTML/JS/CSS, Jquery, AJAX, SQLAlchemy, PostgreSQL, Bootstrap, Pytest MeaningCloud API, LinkPreview API 
