import pytest
import os
from flask import session

from app import create_app
from app.models import db, User, Post, Topics, LinkedTopics


@pytest.fixture(scope='module')
def gen_user():
    User.signup('user1', 'user@email.com', 'password')
    user = User.query.filter_by(username='user1').first()
    return user

@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope='function')
def log_in(test_client):
    test_client.post('/users/login/',
                     data={'username': 'user1',
                           'password': 'password'
                        }, follow_redirects=True)
    yield
    
    test_client.get('/users/logout/', follow_redirects=True)

@pytest.fixture()
def test_queries():
    test_user1 = User.query.filter_by(username='testUser1').first()
    test_user2 = User.query.filter_by(username='testUser2').first()
    return {'user1': test_user1, 
            'user2': test_user2}


@pytest.fixture(scope='module')
def init_database(test_client):

    db.create_all()

    test_user1 = User(
        username='testUser1',
        password='unHashed',
        email='test@email.com'
    )
    test_user2 = User(
        username='testUser2',
        password='unHashed',
        email='test2@email.com'
    )
    db.session.add(test_user1)
    db.session.add(test_user2)

    db.session.commit()

    topic1 = Topics(topic='topic1')
    topic2 = Topics(topic='topic2')
    topic3 = Topics(topic='topic3')

    db.session.add(topic1)
    db.session.add(topic2)
    db.session.add(topic3)

    db.session.commit()

    test_post1 = Post(
        message='mauris commodo quis imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada proin libero nunc consequat interdum varius sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo',
        user_id=test_user1.id,
        sentiment='POSITIVE',
    )
    test_post2 = Post(
        message='mauris commodo quis imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada proin libero nunc consequat interdum varius sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo',
        user_id=test_user2.id,
        sentiment='NEGATIVE'
    )

    test_post3 = Post(
            message='mauris commodo quis imperdiet massa tincidunt nunc pulvinar sapien et ligula ullamcorper malesuada proin libero nunc consequat interdum varius sit amet mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan tortor posuere ac ut consequat semper viverra nam libero justo laoreet sit amet cursus sit amet dictum sit amet justo',
            user_id=test_user2.id,
            sentiment='NEGATIVE',
        )

    db.session.add(test_post1)
    db.session.add(test_post2)
    db.session.add(test_post3)

    db.session.commit()

    db.session.add(LinkedTopics(post_id=test_post1.id, topic_id=topic1.id))
    db.session.add(LinkedTopics(post_id=test_post1.id, topic_id=topic2.id))
    db.session.add(LinkedTopics(post_id=test_post1.id, topic_id=topic3.id))

    db.session.add(LinkedTopics(post_id=test_post2.id, topic_id=topic1.id))
    db.session.add(LinkedTopics(post_id=test_post2.id, topic_id=topic2.id))
    db.session.add(LinkedTopics(post_id=test_post2.id, topic_id=topic3.id))

    db.session.add(LinkedTopics(post_id=test_post3.id, topic_id=topic1.id))
    db.session.add(LinkedTopics(post_id=test_post3.id, topic_id=topic2.id))
    db.session.add(LinkedTopics(post_id=test_post3.id, topic_id=topic3.id))

    db.session.commit()

    yield

    db.close_all_sessions()
    db.drop_all()