from flask import render_template, redirect, session, flash, url_for,g
from sqlalchemy.exc import IntegrityError
from app import CURRENT_USER
from app.users import bp
from app.forms import LoginForm, SignUpForm, CustomizeProfile, deleteProfile
from app.models import db, User, Likes, Post

@bp.before_request
def makeUser_g():
    """Make the current user global"""
    if CURRENT_USER in session:
        g.user = session[CURRENT_USER]
    else:
        g.user = None

def login_success(user):
    session[CURRENT_USER] = user.id

def logout():

    if CURRENT_USER in session:
        del session[CURRENT_USER]

@bp.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            username=form.username.data,
            password=form.password.data,
        )
        if user:
            login_success(user)
            flash(f'Successfully Logged In!', category='success')
            return redirect(url_for("main.homePage"))
        else:
            flash(f'Failed to Log In!', category='danger')
    
    return render_template('users/login.html', form=form)

@bp.route('/signup/', methods=['GET','POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )
            db.session.add(user)
            db.session.commit()
            flash(f'You account has been successfuly made!', category='primary')
            return redirect(url_for("users.login"))
        
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)
    
    return render_template('users/signup.html', form=form)

@bp.route('/logout/')
def logoutRoute():
    """Handle logout of user."""
    logout()
    flash(f'Successfully Logged Out!')
    return redirect('/')

@bp.route('/profile/<int:user_id>')
def userprofile(user_id):
    """View user's profile"""
    user = User.query.get_or_404(user_id)
    user_posts = (Post.query.filter(Post.user_id==user_id)
                    .order_by(Post.timestamp.desc()))
    stat = Likes.query.filter(Likes.user_id==user_id, Likes.agreement>65).all()
    interactions = len(user.comments) + len(user.likedPosts)
    if g.user == user_id:
        return render_template('/users/myuserprofile.html', user=user, stat=stat, user_posts=user_posts, interactions=interactions)
    else:
        return render_template('/users/userprofile.html', user=user, stat=stat, user_posts=user_posts, interactions=interactions)
    
@bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def editprofile(user_id):
    """Get form and edit profile IF g.user is correct"""

    if g.user == user_id:
        user = User.query.get_or_404(user_id)
        form = CustomizeProfile(obj=user)

        if form.validate_on_submit():
            verifieduser = User.authenticate(
                username=user.username,
                password=form.password.data,
            )

            if verifieduser:
                user.username = form.username.data,
                user.bio = form.bio.data,
                user.profile_pic = form.profile_pic.data,
                db.session.commit()
                flash('You account has successfully been updated!', category='success')
                return redirect(f'/users/profile/{user_id}')
            else:
                redirect('/')
        
        return render_template('/users/editprofileform.html', user=user, form=form)
    
    else:
        flash('You are attempting to access something you are not allowed to.', category='warning')
        return redirect('/')

@bp.route('/<int:user_id>/DELETE', methods=['GET', 'POST', 'DELETE'])
def deleteprofile(user_id):

    if g.user == user_id:
        user = User.query.get_or_404(user_id)
        delform = deleteProfile()

        if delform.validate_on_submit():
            verifieduser = User.authenticate(
                username=user.username,
                password=delform.password.data,
            )

            if verifieduser:
                db.session.delete(user)
                db.session.commit()
                return redirect('/users/logout/')
            else:
                flash('You do not have permission.')
                return redirect('/')
        
        return render_template('/users/deleteuserform.html', user=user, delform=delform)
    
    else:
        flash('You are attempting to access something you are not allowed to.', category='warning')
        return redirect('/')