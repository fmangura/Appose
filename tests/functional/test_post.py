from flask import session
from app.models import User, Post, Follows, Likes, LinkedTopics, Connected_Posts, Topics, Comment, db

class TestPostBluePrint():

    def test_GET_getComments(self, test_client, init_database, test_queries, log_in):
        """
        GIVEN Flask app
        WHEN GET '/posts/comments/<id>'
        THEN The post's message is rendered
        """
        user1 = test_queries.get('user1')
        post = Post.query.filter_by(user_id=user1.id).first()
        response = test_client.get(f'/posts/comments/{post.id}')
        
        assert response.status_code == 200
        assert post.message in str(response.data)

    def test_POST_getComments(self, test_client, init_database, test_queries, gen_user, log_in):
        """
        GIVEN Flask app 
        WHEN POST '/posts/comments/<id>'
        THEN A new comment is added to the render
        """
        user1 = test_queries.get('user1')
        post = Post.query.filter_by(user_id=user1.id).first()
        response = test_client.post(f'/posts/comments/{post.id}', 
                                        data={
                                            'post_id': post.id,
                                            'user_id': session['curr_user_id'],
                                            'text': 'TEST COMMENT'
                                        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert post.message in str(response.data)
        assert b'TEST COMMENT' in response.data

    def test_GET_moreOnThis(self, test_client, init_database, test_queries, gen_user, log_in):
        """
        GIVEN Flask app 
        WHEN GET '/posts/<int:post_id>/more'
        THEN all related posts and current post are rendered 
        """
        user1, user2 = test_queries.get('user1'), test_queries.get('user2')
        post1 = Post.query.filter_by(user_id=user1.id).first()
        post2 = Post.query.filter_by(user_id=user2.id).first()

        response = test_client.get(f'/posts/{post1.id}/more')

        assert response.status_code == 200
        assert b'More posts on...' in response.data

        # current post rendered
        assert post1.message in str(response.data)

        # related post rendered
        assert post2.message in str(response.data)

    def test_GET_postAboutPost(self, test_client, init_database, test_queries, gen_user, log_in):
        """
        GIVEN Flask app 
        WHEN GET '/posts/<int:post_id>/response'
        THEN all related posts and current post are rendered 
        """
        user1 = test_queries.get('user1')
        post = Post.query.filter_by(user_id=user1.id).first()

        response = test_client.get(f'/posts/{post.id}/response')

        assert response.status_code == 200
        assert post.message in str(response.data)
        assert b'Whats on your mind...' in response.data

    def test_POST_postAboutPost(self, test_client, init_database, test_queries, gen_user, log_in):
        """
        GIVEN Flask app 
        WHEN POST '/posts/<int:post_id>/response'
        THEN redirected to original post is rendered and new post is made
        """
        user1 = test_queries.get('user1')
        post = Post.query.filter_by(user_id=user1.id).first()

        response = test_client.post(f'/posts/{post.id}/response', data={
            'user_id': gen_user.id,
            'message':'TEST RESPONSE POST TO A SINGLE POST sit amet porttitor eget dolor'}, follow_redirects=True)

        # Check if returned to Comment post
        assert response.status_code == 200
        assert b'Make Comment...' in response.data

        # Check if response post is made in home route
        response = test_client.get('/')
        assert b'response to' in response.data
        assert b'TEST RESPONSE POST TO A SINGLE POST' in response.data

    def test_DELETE_deletePost(self, test_client, init_database, test_queries, gen_user, log_in):
        """
        GIVEN Flask app and correct user
        WHEN DELETE '/posts//<int:post_id>/delete'
        THEN post no longer in home route
        """
        # Make test post
        post = Post(
            message='TEST OF NEW POST commodo quis imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada proin',
            user_id=gen_user.id,
            )
        db.session.add(post)
        db.session.commit()

        # Check if post in home
        home = test_client.get('/')
        assert post.message in str(home.data)

        # Deletes post
        response = test_client.get(f'/posts/{post.id}/delete', follow_redirects=True)

        # Check if post not in home, successfully deleted
        home = test_client.get('/')
        assert post.message not in str(home.data)

    def test_DELETE_deletePost_WRONGuser(self, test_client, init_database, test_queries, gen_user, log_in):
        """
        GIVEN Flask app and incorrect user
        WHEN DELETE '/posts//<int:post_id>/delete'
        THEN post still in home route
        """
        not_loggedin_user = test_queries.get('user1')
        # Make test post
        post = Post(
            message='TEST OF NEW POST commodo quis imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada proin',
            user_id=not_loggedin_user.id,
            )
        db.session.add(post)
        db.session.commit()

        # Check if post in home
        home = test_client.get('/')
        assert post.message in str(home.data)

        # Deletes post
        response = test_client.get(f'/posts/{post.id}/delete', follow_redirects=True)
        assert b'You do not have permission to delete' in response.data
        assert post.message in str(response.data)
        
