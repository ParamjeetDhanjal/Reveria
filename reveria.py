import os
import uuid
from datetime import datetime
from flask_migrate import Migrate
from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "reveria_ultimate_v5_2026"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reveria.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --- MODELS --- #

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profile_pic = db.Column(db.String(100), default='default.jpg')
    is_private = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete")
    likes = db.relationship('Like', backref='user', lazy=True)
    followed = db.relationship('User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self, password): self.password_hash = generate_password_hash(password)
    def check_password(self, password): return check_password_hash(self.password_hash, password)
    def is_following(self, user): return self.followed.filter(followers.c.followed_id == user.id).count() > 0

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(200))
    music_file = db.Column(db.String(100))
    music_start = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    media = db.relationship('Media', backref='post', cascade="all, delete")
    likes = db.relationship('Like', backref='post', cascade="all, delete")
    comments = db.relationship('Comment', backref='post', cascade="all, delete")

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

class FollowRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user = db.relationship('User', backref='user_comments')
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

# --- ROUTES --- #

@app.route('/')
def index():
    if 'username' in session: return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login/', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username']).first()
    if user and user.check_password(request.form['password']):
        session['username'] = user.username
        return redirect(url_for('home'))
    return redirect(url_for('index'))
@app.route('/signup', methods=['GET'])
def redirect_signup():
    return render_template("signup.html")
@app.route('/signup/', methods=['POST'])
def signup():
    if User.query.filter_by(username=request.form['username']).first(): return "Username taken"
    user = User(name=request.form['name'], username=request.form['username'], email=request.form['email'])
    user.set_password(request.form['password'])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/home/')
def home():
    if 'username' not in session:
        return redirect('/')

    me = User.query.filter_by(username=session['username']).first()

    if me is None:
        session.clear()
        return redirect(url_for('index'))

    search_q = request.args.get('q', '')
    search_results = []

    if search_q:
        search_results = User.query.filter(User.username.contains(search_q)).all()

    following_ids = [u.id for u in me.followed.all()]
    following_ids.append(me.id)

    posts = (
        Post.query
        .join(User)
        .filter(
            (User.id.in_(following_ids)) |
            (User.is_private == False)
        )
        .order_by(Post.created_at.desc())
        .all()
    )

    return render_template(
        'home.html',
        user=me,
        posts=posts,
        search_results=search_results,
        q=search_q
    )


@app.route('/upload', methods=['POST'])
def upload():
    user = User.query.filter_by(username=session['username']).first()
    images = request.files.getlist('images')
    song = request.files.get('song')
    post = Post(caption=request.form.get('caption'), author=user, music_start=int(request.form.get('music_start', 0)))
    
    if song and song.filename:
        fn = f"music_{uuid.uuid4().hex}.mp3"
        song.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
        post.music_file = fn
        m_start = request.form.get('music_start')
        music_start_val = int(m_start) if m_start and m_start.isdigit() else 0
        
        post = Post(
            caption=request.form.get('caption'), 
            author=user, 
            music_start=music_start_val)
    for img in images:
        if img.filename:
            fn = f"img_{uuid.uuid4().hex}.jpg"
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
            post.media.append(Media(filename=fn))
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    me = User.query.filter_by(username=session.get('username')).first()
    return render_template('post.html', post=post, me=me)

@app.route('/follow/<int:user_id>', methods=['POST'])
def follow(user_id):
    me = User.query.filter_by(username=session['username']).first()
    target = User.query.get_or_404(user_id)

    if me.id == target.id or me.is_following(target):
        return redirect(request.referrer)

    if target.is_private:
        existing = FollowRequest.query.filter_by(
            from_user_id=me.id,
            to_user_id=target.id
        ).first()

        if not existing:
            db.session.add(FollowRequest(
                from_user_id=me.id,
                to_user_id=target.id
            ))
            db.session.commit()
    else:
        me.followed.append(target)
        db.session.commit()

    return redirect(request.referrer)

@app.route('/notifications')
def notifications():
    me = User.query.filter_by(username=session.get('username')).first()
    if not me:
        return redirect('/login')

    requests = FollowRequest.query.filter_by(to_user_id=me.id).all()

    # MANUAL JOIN (since you refuse relationships)
    request_data = []
    for r in requests:
        sender = User.query.get(r.from_user_id)
        request_data.append({
            "id": r.id,
            "sender": sender
        })

    return render_template(
        "notifications.html",
        requests=request_data
    )
@app.route('/accept-request/<int:req_id>', methods=['POST'])
def accept_request(req_id):
    req = FollowRequest.query.get_or_404(req_id)
    me = User.query.filter_by(username=session['username']).first()

    if req.to_user_id != me.id:
        return "Unauthorized", 403

    follower = User.query.get(req.from_user_id)
    follower.followed.append(me)   # ✅ CORRECT

    db.session.delete(req)
    db.session.commit()

    return redirect('/notifications')

@app.route('/upload-profile-pic', methods=['POST'])
def upload_profile_pic():
    if 'username' not in session:
        return redirect(url_for('index'))

    user = User.query.filter_by(username=session['username']).first()
    file = request.files.get('profile_pic')

    if not file:
        return redirect(url_for('profile', username=user.username))

    filename = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join('static/profile', filename)
    file.save(path)

    user.profile_pic = filename
    db.session.commit()

    return redirect(url_for('profile', username=user.username))

@app.route('/decline-request/<int:req_id>', methods=['POST'])
def decline_request(req_id):
    req = FollowRequest.query.get_or_404(req_id)

    me = User.query.filter_by(username=session['username']).first()

    if req.to_user_id != me.id:
        return "Unauthorized", 403

    db.session.delete(req)
    db.session.commit()

    return redirect('/notifications')

@app.route('/profile/<username>')
def profile(username):
    me = User.query.filter_by(username=session.get('username')).first()
    user = User.query.filter_by(username=username).first_or_404()
    tab = request.args.get('tab', 'posts')

    is_owner = me and me.id == user.id
    is_following = me and me.is_following(user)

    # PRIVATE ACCOUNT LOGIC
    if user.is_private and not is_owner and not is_following:
        request_sent = False
        if me:
            request_sent = FollowRequest.query.filter_by(
                from_user_id=me.id,
                to_user_id=user.id
            ).first() is not None

        return render_template(
            'private.html',
            user=user,
            me=me,
            request_sent=request_sent
        )

    # FOLLOWERS & FOLLOWING
    followers = user.followers.all()  # who follows this user
    following = user.followed.all()   # who this user follows

    liked_posts = (
        Post.query
        .join(Like)
        .filter(Like.user_id == user.id)
        .all()
    )

    return render_template(
        'profile.html',
        user=user,
        me=me,
        tab=tab,
        is_following=is_following,
        followers=followers,
        following=following,
        liked_posts=liked_posts
    )



@app.route('/follow-request/<int:user_id>', methods=['POST'])
def send_follow_request(user_id):
    sender = User.query.filter_by(username=session['username']).first()

    if not FollowRequest.query.filter_by(
        from_user_id=sender.id,
        to_user_id=user_id
    ).first():
        db.session.add(
            FollowRequest(
                from_user_id=sender.id,
                to_user_id=user_id
            )
        )
        db.session.commit()

    return redirect(request.referrer)

@app.route('/explore')
def explore():
    posts = (
        Post.query
        .join(User)
        .filter(User.is_private == False)
        .order_by(Post.created_at.desc())
        .all()
    )
    return render_template('explore.html', posts=posts)

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    user = User.query.filter_by(username=session['username']).first()
    l = Like.query.filter_by(user_id=user.id, post_id=post_id).first()
    if l: db.session.delete(l)
    else: db.session.add(Like(user_id=user.id, post_id=post_id))
    db.session.commit()
    return redirect(request.referrer)

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    user = User.query.filter_by(username=session['username']).first()
    parent_id = request.form.get('parent_id')
    db.session.add(Comment(text=request.form['text'], user_id=user.id, post_id=post_id, parent_id=parent_id if parent_id else None))
    db.session.commit()
    return redirect(request.referrer)

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.username == session['username']:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/unfollow/<int:user_id>', methods=['POST'])
def unfollow(user_id):
    me = User.query.filter_by(username=session['username']).first()
    target = User.query.get(user_id)
    if me.is_following(target):
        me.followed.remove(target)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    user = User.query.filter_by(username=session['username']).first()
    file = request.files.get('profile_pic')
    if file and file.filename:
        fn = f"pfp_{uuid.uuid4().hex}.jpg"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
        user.profile_pic = fn
    user.is_private = 'is_private' in request.form
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.clear(); return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context(): db.create_all()
    app.run(debug=True)