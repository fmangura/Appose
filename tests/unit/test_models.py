from app.models import User, Post, Follows, Likes, LinkedTopics, Connected_Posts, Topics, Comment, db

import pytest
     
class TestUserModel():

    def test_signup_authenticate(self, test_client):
        """
        GIVEN a registered User
        WHEN a user is signedup
        THEN check if user is authorized
        """
        new_user = User.signup(username='registerUser', email='register@email.com',password='hashedpass')

        authUser = User.authenticate(username='registerUser', password='hashedpass')

        wrongUser = User.authenticate(username='registerUser', password='wrong')

        assert authUser == new_user
        assert wrongUser == False

    def test_startfollow(self, init_database):
        """
        GIVEN startfollows method
        WHEN a user follows another
        THEN check function is successful
        """
        # Query users
        user1 = User.query.filter(User.username=='testUser1').first()
        user2 = User.query.filter_by(username='testUser2').first()

        # Use startfollows (id, id) function
        User.startfollow(user1.id, user2.id)

        # Query follow database
        beingFollowed = Follows.query.filter_by(user_followed_id=user2.id).first()
        following = Follows.query.filter_by(user_following_id=user1.id).first()

        # Check if function was successful
        assert beingFollowed.user_followed_id == user2.id
        assert following.user_following_id == user1.id

class TestPostsModel():

    def test_makePost(self, gen_user):
        """
        GIVEN a user_id and message
        WHEN makePost is called
        THEN check if post is successfully created AND API is connected
        """
        message = 'justo eget magna fermentum iaculis eu non diam phasellus vestibulum lorem sed risus ultricies tristique nulla aliquet enim tortor at auctor urna nunc id cursus metus aliquam eleifend mi in nulla posuere sollicitudin aliquam ultrices sagittis orci a scelerisque purus semper eget duis at tellus at urna condimentum mattis pellentesque'

        user = gen_user

        Post.makePost(user_id=user.id, message=message, link='')

        post = Post.query.filter_by(user_id=user.id).first()

        assert post.user_id == user.id
        assert post.message == message
        assert post.sentiment_data['status']['test'] == True
        assert post.sentiment_data['status']['msg'] == 'TEST DATA; API CALL VERY LIMITED'

    def test_lookSameTopicPosts(self, test_queries):
        """
        GIVEN two posts share the same topics
        WHEN function is called on post1
        THEN receive back an array where post2 is in array
        """
        user1, user2 = test_queries.get('user1'), test_queries.get('user2')

        post1 = Post.query.filter_by(user_id=user1.id).first()
        post2 = Post.query.filter_by(user_id=user2.id).first()

        posts = Post.lookForSameTopicPosts(post1)
        assert post2 in posts

    def test_findSameTopicPosts(self, test_queries):
        """
        GIVEN two posts share the same topics AND relevant = True
        WHEN function is called on post1
        THEN Connected_Posts table is updated with linked_by == 'TOPICS'
        """
        user1, user2 = test_queries.get('user1'), test_queries.get('user2')

        post_1 = Post.query.filter_by(user_id=user1.id).first()
        post_2 = Post.query.filter_by(user_id=user2.id).all()[0]
        post_3 = Post.query.filter_by(user_id=user2.id).all()[1]

        # When relevance == True for only 1 post, no match is made and no array is found
        post_1.relevance = True
        db.session.commit()

        Post.findSameTopicPosts(post_1)
        connection = Connected_Posts.query.filter_by(post1=post_1.id).first()

        assert connection is None

        # When relevance == True in 2 posts, a match is made and found in Connected_Posts
        post_2.relevance = True
        db.session.commit()

        Post.findSameTopicPosts(post_1)
        connection = Connected_Posts.query.filter_by(post1=post_1.id).first()

        assert connection.post2 == post_2.id
        assert connection.post1 == post_1.id
        assert connection.linked_by == 'TOPICS'

        # More than 1 connection can be made
        post_3.relevance = True
        db.session.commit()

        Post.findSameTopicPosts(post_1)
        connection = Connected_Posts.query.filter_by(post1=post_1.id).all()
        assert len(connection) == 2

class TestLikesModel():

    def test_Likes_table(self, test_queries):
        """
        GIVEN Likes data
        WHEN doing User & Post methods with relationship to Likes table
        THEN get list of Liked Posts for Users and Agreement of a particular user for that Post
        """

        user1, user2 = test_queries.get('user1'), test_queries.get('user2')
        post_2 = Post.query.filter_by(user_id=user2.id).first()

        like = Likes(user_id=user1.id, post_id=post_2.id, agreement=40)

        db.session.add(like)
        db.session.commit()

        # Test post id is found in user's list of Liked Posts
        assert post_2.id in user1.getLikedPosts()

        # Test user's agreement is returned when post getUsersAgreement func is called
        assert post_2.getUsersAgreement(user1.id) == like.agreement

class TestCommentModel():

    def test_Comment_created(self, test_queries):
        """
        GIVEN comment data is made
        WHEN comment is being searched
        THEN both comment table, post.comment, user.comments will return comment
        """

        user1, user2 = test_queries.get('user1'), test_queries.get('user2')
        post_2 = Post.query.filter_by(user_id=user2.id).first()

        new_comment = Comment(text='TEST COMMENT', post_id=post_2.id, user_id=user1.id)
        db.session.add(new_comment)
        db.session.commit()

        comment = Comment.query.filter_by(text=new_comment.text).first()

        # Test table
        assert comment is new_comment

        # Test comment in Post
        assert new_comment in post_2.comments

        # Test comment in User
        assert new_comment in user1.comments






