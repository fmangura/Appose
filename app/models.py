from datetime import datetime
from flask import flash, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from statistics import mean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
import requests
import random


MEANINGCLOUD_BASE = 'https://api.meaningcloud.com/'
MEANINGCLOUD_KEY = '06beae76af6e887023bdb2edc872888a'

POS_SENTIMENT = ['P+', 'P']
NEG_SENTIMENT = ['N+', 'N']

bcrypt = Bcrypt()
db = SQLAlchemy()


# Models: Post, User, Topic

############# 
    
# Follows Model
    
#############
    
class Follows(db.Model):

    __tablename__ = 'follows'

    user_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,
    )

    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True,
    )

############# 
    
# Likes Model
    
#############

class Likes(db.Model):

    __tablename__ = 'likes'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', ondelete='CASCADE'),
        primary_key=True
    )

    agreement = db.Column(
        db.Integer,
        default=50,
        primary_key=True
    )

############# 
    
# Topics Link Model
    
#############
    
class LinkedTopics(db.Model):

    __tablename__ = 'linkedtopics'

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', ondelete='CASCADE'),
        primary_key=True,
    )

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey('topics.id', ondelete='CASCADE'),
        primary_key=True,
    )

############# 
    
# Connected_Posts Model
    
#############
    
class Connected_Posts(db.Model):
    """NOTICE: post1 = responding_to; post2 = responses. 
        This means: when using post.responses, we are checking if there is a Connected_Post model with that post as post1. We return/get back all posts that are in post2 of that model."""

    __tablename__ = 'connected_posts'

    id = db.Column(
        db.Integer,
        unique=True,
        autoincrement=True,
    )

    post1 = db.Column(
        db.ForeignKey('posts.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
    )

    post2 = db.Column(
        db.ForeignKey('posts.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
    )

    linked_by = db.Column(
        db.Text,
    )

    comments = db.relationship('CommentForCP', backref='post', cascade='all, delete-orphan')

@classmethod
def makeConnection(cls, post1, post2):
    connect = Connected_Posts(post1=post1, post2=post2, linked_by='RELEVANCE')
    db.session.add(connect)
    db.session.commit()
    
############# 
    
# Post Model
    
#############

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    message = db.Column(
        db.Text,
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User', backref='posts')

    sentiment_data = db.Column(
        JSONB,
        default=None
    )

    sentiment = db.Column(
        db.Text,
        default='Neutral',
    )

    header_img = db.Column(
        db.Text,
    )

    relevance = db.Column(
        db.Boolean,
        default=False,
    )

    link = db.Column(
        db.Text,
    )

    linkPreview = db.Column(
        JSONB,
        default=None
    )

    topics = db.relationship('Topics',
                             secondary='linkedtopics',
                             backref='posts',
                             cascade='all, delete'
                        )

    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan')

    """Looks in Connected_Posts.post1 column for this id. 
        Think: SELECT * FROM Connected_Posts WHERE post1 = post.id """
    responses = db.relationship("Connected_Posts",
        foreign_keys=[Connected_Posts.post1],
        backref=db.backref('responding_to', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    
    """Looks in Connected_Posts.post2 column for this id. 
        Think: SELECT * FROM Connected_Posts WHERE post2 = post.id """
    responding_to = db.relationship("Connected_Posts",
        foreign_keys=[Connected_Posts.post2],
        backref=db.backref('responses', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')
    
    # def getMostRelevantToPost(self):
    #     """Get the most relevant post response"""
    #     if self.responses:
    #         post = (Connected_Posts.query
    #                 .filter(Connected_Posts.post1==self.id).all())
    #         ran = random.randint(0, len(post)-1)
    #         posts = post[ran]
    #         return posts

    def getTopic(self):
        """Use data to get topic of the message"""
        data = self.sentiment_data
        if data["status"]["code"] == '0':
            print(data["sentimented_entity_list"])

            entities = [entity["form"] for entity in data["sentimented_entity_list"]]

            for topic in entities:
                allTopics = [named_topic.topic for named_topic in Topics.query.all()]

                if topic in allTopics:
                    new_topic = Topics.query.filter_by(topic=f'{topic}').first()
                else:
                    new_topic = Topics(topic=f'{topic}')
                    db.session.add(new_topic)
                    db.session.commit()

                if LinkedTopics.query.filter_by(post_id=self.id, topic_id=new_topic.id).first():
                    continue
                else:
                    linkTopic = LinkedTopics(post_id=self.id, topic_id=new_topic.id)
                    db.session.add(linkTopic)
                    db.session.commit()
        return

    def getLinkPreview(self):
        """Get link to make link preview accessing an API ONLY IF it has not been linked before"""
        link = Post.query.filter_by(link=self.link).all()
        if link:
            firstlinkpreview = Post.query.filter_by(link=self.link).first()
            self.linkPreview = firstlinkpreview.linkPreview
            db.session.commit()
        res = requests.post('https://api.linkpreview.net',
                            headers={
                                'X-Linkpreview-Api-Key': 'af4da178126dd4142d9758ef6a13d829'},
                            params={'q': self.link}
                        )
        data = res.json()
        self.linkPreview = data
        db.session.commit()

    def allTopics(self):
        """Make list of the topics"""
        topicsList = [topics.topic for topics in self.topics]
        return topicsList

    def getSentimentData(self):
        """Use API to get sentiment of the message"""
        try:
            res = requests.post(f'{MEANINGCLOUD_BASE}sentiment-2.1',
                                params={
                                    'key': MEANINGCLOUD_KEY,
                                    'lang': 'auto',
                                    'egp': 'y',
                                    'uw': 'y',
                                    'txt': self.message,
                                })
            data = res.json()
            self.sentiment_data = data
            db.session.commit()
        except IntegrityError:
            return flash(f'No data was retrieved')

    def getOverallSentiment(self):
        """Assess sentiment to be 'Positive' or 'Negative'"""
        if self.sentiment_data['status']['code'] == '0':
            sentiment = self.sentiment_data['score_tag']
            if sentiment in ['P+', 'P']:
                self.sentiment = 'POSITIVE'
                db.session.commit()

            elif sentiment in ['N+', 'N']:
                self.sentiment = 'NEGATIVE'
                db.session.commit()
            else:
                return
        else:

            return
        return
        
    def listtopics(self):
        """Find and connect posts"""
        topics = [topic.topic for topic in self.topics]
        return topics
    
    def sumInteractions(self):
        """Sum up all likes and comments"""
        totalInteractions = len(self.liked_by) + len(self.comments)
        return totalInteractions
    
    def checkRelevance(self):
        """After the post is liked > check sumInteractions if >= 5 (changeable) > make relevance True > search for posts that share same topic & relevance status"""
        relevance_score = self.sumInteractions()
        if relevance_score < 10:
            return
        else:
            post = Post.query.get(self.id)

            if self.relevance == True:
                Post.findSameTopicPosts(post)
            else:
                self.relevance = True
                db.session.commit()
                Post.findSameTopicPosts(post)
                return

    def getUsersAgreement(self, user_id):
        """Get the value that the user input"""
        agreed = Likes.query.filter_by(post_id=self.id, user_id=user_id).first()
        if agreed:
            return agreed.agreement
        else:
            return 50
        
    def getAvgAgreement(self):
        """Get the average of agreements"""
        likes = [agreements.agreement for agreements in Likes.query.filter_by(post_id=self.id)]
        
        stats = round(mean(likes),0)
        return stats
    
    def getStrAgree(self):
        """Get the percentage of agreements"""
        agree = Likes.query.filter(Likes.post_id==self.id, Likes.agreement > 80).all()
        all = Likes.query.filter_by(post_id=self.id).all()

        stats = len(agree)/len(all) * 100
        return stats
    
    def getdisAgree(self):
        """Get the percentage of disgreements"""
        against = Likes.query.filter(Likes.post_id==self.id, Likes.agreement < 20).all()
        all = Likes.query.filter_by(post_id=self.id).all()

        stats = len(against)/len(all) * 100
        return stats
        
    @classmethod
    def findSameTopicPosts(cls, post):
        """Searchings for topics when posts are relevant to create Connected_Posts Model. Unlike its counterpart, this does not affect templates."""
        print(f'{post}<<<<This is the post being checked on')
        post1Topics = post.allTopics()
        print(f'{post1Topics}<<<< These are its topics')
        allposts = Post.query.filter(Post.relevance==True, Post.user_id!=post.user_id).all()
        print(f'{allposts}<<<<<These are the posts {post} is being compared to')

        for post2 in allposts:
            checklinks = Connected_Posts.query.filter(Connected_Posts.post1==post.id, Connected_Posts.post2==post2.id).all()
            print([resp for resp in post2.responses])
            print([resp for resp in post2.responding_to])

            if checklinks:
                print(f'{post} and {post2} are already linked')
                continue

            else:
                compare = set(post1Topics).intersection(set(post2.allTopics()))

                if len(compare) >= 1:
                    connect = Connected_Posts(post1=post.id, post2=post2.id, linked_by='TOPICS')
                    db.session.add(connect)
                    db.session.commit()
                    print('connection made')
                else:
                    continue

    @classmethod
    def lookForSameTopicPosts(cls, post):
        """For rendering non-relevant same topics in the /more route"""
        post1Topics = post.allTopics()
        print(f'{post1Topics}<<<<< LOOKING FOR THESE TOPICS')
        allposts = Post.query.filter(Post.id != post.id).all()
        sameTopics = [];

        for post2 in allposts:
            print(f'{post2.allTopics()}<<<<< TOPICS FOUND')
            compare = set(post1Topics).intersection(set(post2.allTopics()))
            print(compare)
            if len(compare) >= 1:
                sameTopics.append(post2);
            else:
                continue
        
        print(sameTopics)
        return sameTopics;


    @classmethod
    def makePost(cls, user_id, message, link):
        if message:
            post = Post(user_id=user_id, message=message, link=link)
            db.session.add(post)
            db.session.commit()
            post.getSentimentData()
            if link:
                post.getLinkPreview()
            post.getOverallSentiment()
            post.getTopic()

            return post
        
    # @classmethod
    # def compareTopics(cls, compare_to):
    #     otherPosts_list = Post.query.

############# 
    
# Users Model
    
#############

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    
    password = db.Column(
        db.Text,
        nullable=False,
    )

    bio = db.Column(
        db.Text,
    )

    location = db.Column(
        db.Text,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    profile_pic = db.Column(
        db.Text,
        default='/static/images/noimg.png',
    )

    email_validity = db.Column(
        db.Boolean,
        default=False,
    )

    admin_status = db.Column(
        db.Boolean,
        default=False,
    )

    userpost = db.relationship('Post', cascade='all, delete')

    likedPosts = db.relationship('Post', secondary='likes', cascade='all, delete', backref='liked_by')

    comments = db.relationship('Comment', backref='user', cascade='all, delete')

    followers = db.relationship("Follows",
        foreign_keys=[Follows.user_followed_id],
        backref=db.backref('following', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    following = db.relationship("Follows",
        foreign_keys=[Follows.user_following_id],
        backref=db.backref('followers', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')


    def __repr__(self):
        return f"User id: {self.id}, username: {self.username}"
    
    def follow(self, user):
        if not self.following(user):
            f = Follows(follower=self, following=user)
            db.session.add(f)
    
    def unfollower(self, user):
        f = self.following.filter_by(user_following_id=user.id).first()
        db.session.delete(f)

    def getLikedPosts(self):
        return [post.id for post in self.likedPosts]


    @classmethod
    def signup(cls, username, email, password):
        """ Sign up user using Hasing password """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            profile_pic='/static/images/noimg.png',
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """ Find user with username and password. """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    @classmethod
    def startfollow(cls, curr_userID, to_followID):
        """Current user follows other user. """
        follow = Follows(user_followed=to_followID, user_following=curr_userID)
        db.session.add(follow)
        db.session.commit()

  
############# 
    
# Topics Model
    
#############

class Topics(db.Model):

    __tablename__ = 'topics'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    topic = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )



    

############# 
    
# Comments Model
    
#############
    
class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('posts.id', ondelete='CASCADE')
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )

class CommentForCP(db.Model):

    __tablename__ = 'commentsforcp'

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
    )

    text = db.Column(
        db.Text,
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey('connected_posts.id', ondelete='CASCADE')
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE')
    )
    

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)