from app.main import bp
from app.models import db, User, Post, Comment, Likes
from app.forms import CreatePost, CreateComment, AgreementForm
from flask import render_template, g, session, redirect, url_for, jsonify, request
from app import CURRENT_USER

@bp.before_request
def makeUser_g():
    """Make the current user global"""
    if CURRENT_USER in session:
        g.user = session[CURRENT_USER]
    else:
        g.user = None

@bp.route('/', methods=['GET','POST'])
def homePage():
    """Route for going home page"""
    if g.user:
        user = User.query.get(g.user)
        posts = (Post.query
                    .order_by(Post.timestamp.desc())
                    .all())
        new_post_form = CreatePost()
        if new_post_form.validate_on_submit():
            post = Post.makePost(
                user_id=g.user,
                message=new_post_form.message.data,
                link=new_post_form.link.data,
            )
            return redirect(url_for("main.homePage"))
  
        return render_template('home.html', user=user, posts=posts, new_post_form=new_post_form)
    
    return render_template('landingpage.html')

@bp.route('/agreement', methods=['POST'])
def changeAgreement():
    """Add value to agreement"""
    post_id = request.json['post_id']
    value = request.json['input_value']
    post = Post.query.get_or_404(post_id)

    if g.user:
        like = Likes.query.filter_by(user_id=g.user, post_id=post_id).first()
        
        if like:
            like.agreement = value
            db.session.commit()
            post.checkRelevance()
            return ('', 204)
        else:
            like = Likes(user_id=g.user, post_id=post_id, agreement=value)
            db.session.add(like)
            db.session.commit()
            if post.relevance == False:
                post.checkRelevance()
            return ('', 204)