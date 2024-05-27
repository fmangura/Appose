from flask import render_template, redirect, session, flash, url_for, jsonify, g
from sqlalchemy.exc import IntegrityError
from app import CURRENT_USER
from app.posts import bp
from app.forms import LoginForm, SignUpForm, CreateComment, CreatePost
from app.models import db, User, Comment, Post, Likes, Connected_Posts

@bp.before_request
def makeUser_g():
    """Make the current user global"""
    if CURRENT_USER in session:
        g.user = session[CURRENT_USER]
    else:
        g.user = None

@bp.route('/categories/')
def categories():
    return render_template('posts/categories.html')

@bp.route('/comments/<int:post_id>', methods=['GET','POST'])
def getComments(post_id):

    post = Post.query.get(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    form = CreateComment()

    if g.user:
        if form.validate_on_submit():
            addComment = Comment(
                post_id=post_id,
                user_id=g.user,
                text=form.text.data
            )
            db.session.add(addComment)
            db.session.commit()
            return redirect(f'/posts/comments/{post_id}')
        
    return render_template('/posts/fullPost.html', form=form, post=post, comments=comments)

@bp.route('/like/<int:post_id>', methods=['POST'])
def likePost(post_id):
    if g.user:
        post = Post.query.get(post_id)
        like = Likes.query.filter_by(post_id=post_id, user_id=g.user).first()
        if not like:
<<<<<<< HEAD
            print('Making Likes')
=======
>>>>>>> e7e0204 (Added Testing)
            doLike = Likes(post_id=post_id, user_id=g.user)
            db.session.add(doLike)
            db.session.commit()
        
        if post.relevance == True:
            return redirect('/')
        else:
            post.checkRelevance()
            return redirect('/')

@bp.route('/like/<int:post_id>/delete', methods=['GET','DELETE'])
def deleteLike(post_id):
    if g.user:
        like = Likes.query.filter_by(post_id=post_id, user_id=g.user).first()
        db.session.delete(like)
        db.session.commit()
        return ('', 204)

@bp.route('/<int:post_id>/more')
def moreOnThis(post_id):
    post = Post.query.get_or_404(post_id)
    posts_on_link = Post.query.filter_by(link=post.link).all()
    main_post = Connected_Posts.query.filter(Connected_Posts.post1==post_id).all()
    same_topics = Post.lookForSameTopicPosts(post)
    if g.user:
        return render_template('/posts/moreOnThis.html',
                               post=post,
                               posts_on_link=posts_on_link,
                               main_post=main_post,
                               same_topics=same_topics,
                            )
    

@bp.route('/<int:post_id>/response', methods=['GET', 'POST'])
def postAboutPost(post_id):
    form = CreatePost()
    post = Post.query.get_or_404(post_id)

    if g.user:
        if form.validate_on_submit():
            response = Post.makePost(
                    user_id=g.user,
                    message=form.message.data,
                    link=None
                )
            db.session.add(response)
            db.session.commit()

            response.link = post.link
            response.linkPreview = post.linkPreview
            db.session.commit()

            connect = Connected_Posts(post1=post.id, post2=response.id, linked_by='RESPONDED')

            db.session.add(connect)
            db.session.commit()

            return redirect(f'/posts/comments/{post.id}')

        return render_template('/posts/respond.html', form=form, post=post)
    
@bp.route('/<int:post_id>/delete', methods=['GET','DELETE'])
def deletePost(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id == g.user:
        db.session.delete(post)
        db.session.commit()
        return ('', 204)
    else:
<<<<<<< HEAD
        flash('You do not have permission to delete')
=======
        flash('You do not have permission to delete', category='danger')
>>>>>>> e7e0204 (Added Testing)
        return redirect('/')

