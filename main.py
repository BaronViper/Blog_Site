from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy.orm import relationship
from forms import LoginForm, BlogForm, SubjectForm, SearchForm
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
import dotenv
import os

dotenv.load_dotenv()
date = datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRES_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    posts = relationship("BlogPost", back_populates="author")


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"))
    subject = relationship("Subject", back_populates="blogs")

    quote = db.Column(db.String(250), nullable=False)
    quote_author = db.Column(db.String(250), nullable=False)

    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(250), nullable=False)

    quote = db.Column(db.String(250), nullable=False)

    birth = db.Column(db.Integer, nullable=False)
    death = db.Column(db.Integer, nullable=False)
    biography = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    visibility = db.Column(db.String(250), nullable=False)

    blogs = relationship("BlogPost", back_populates="subject")


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 6

    if not BlogPost.query.all():
        all_posts = False
        featured_post = 0

    elif page == 1 and BlogPost.query.all():
        featured_post = BlogPost.query.order_by(BlogPost.id.desc()).first()
        all_posts = BlogPost.query.filter(BlogPost.id != featured_post.id).order_by(BlogPost.id.desc()).paginate(
            page=page, per_page=per_page)
    else:
        featured_post = 0
        all_posts = BlogPost.query.filter(
            BlogPost.id != BlogPost.query.order_by(BlogPost.id.desc()).first().id).order_by(
            BlogPost.id.desc()).paginate(
            page=page, per_page=per_page)

    return render_template('index.html', featured_post=featured_post, all_posts=all_posts)


# @app.route('/search/<search>', methods=['GET'])
# def search(keyword):
#     pass


@app.route('/post/<int:post_id>', methods=['GET'])
def blog(post_id):
    target_post = BlogPost.query.filter_by(id=post_id).first()
    return render_template('post.html', post=target_post)


@app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@app.route('/search', methods=['POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        print(type(BlogPost.query.filter(BlogPost.title.like('%' + form.searched.data + '%'))))
        page = request.args.get(get_page_parameter(), type=int, default=1)
        posts = BlogPost.query.filter(BlogPost.title.like('%' + form.searched.data + '%')).order_by(
            BlogPost.title).paginate(
            page=page, per_page=6)

        return render_template('search.html', form=form, all_posts=posts)
    return redirect(url_for('home'))


@app.route('/subjects')
def subjects():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 6

    if not Subject.query.filter_by(visibility="1").all():
        all_posts = False
        featured_post = 0

    elif page == 1 and Subject.query.filter_by(visibility="1").all():
        visible_posts = Subject.query.filter_by(visibility="1").order_by(Subject.id.desc()).all()
        featured_post = visible_posts[0]
        all_posts = Subject.query.filter(Subject.id != featured_post.id, Subject.visibility == "1").order_by(
            Subject.id.desc()).paginate(
            page=page, per_page=per_page)
    else:
        featured_post = 0
        all_posts = Subject.query.filter(
            Subject.id != Subject.query.order_by(Subject.id.desc()).first().id).order_by(
            Subject.id.desc()).paginate(
            page=page, per_page=per_page)

    return render_template('subjects.html', featured_post=featured_post, all_posts=all_posts)


@app.route('/subject/<int:subject_id>', methods=['GET'])
def subject(subject_id):
    target_post = Subject.query.filter_by(id=subject_id).first()
    return render_template('subject.html', post=target_post)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.name.data
        if User.query.filter_by(name=name).first():
            password = form.password.data
            user = User.query.filter_by(name=name).first()
            if check_password_hash(user.password, password):
                login_user(user)
            else:
                flash(message='Incorrect Password')
                return redirect(url_for('login'))
        else:
            flash(message='Invalid User')
            return redirect(url_for('login'))
        return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create', methods=["POST", "GET"])
@login_required
def create():
    form = BlogForm()
    all_subjects = db.session.query(Subject).all()
    form.subject.choices += [(subject.name, subject.name) for subject in all_subjects if
                             (subject.name, subject.name) not in form.subject.choices]

    if form.validate_on_submit():
        if form.subject.data == "":
            flash(message="Blog must focus on an already registered person. If no person is found in drop down list, "
                          "add one!")
            return redirect(url_for('create'))
        if BlogPost.query.filter_by(title=form.title.data.title()).first():
            flash(message="Blog post with this title already exists. Please rename your blog.")
            return redirect(url_for('create'))
        selected_subject = Subject.query.filter_by(name=form.subject.data).first()
        new_post = BlogPost(
            title=form.title.data.title(),
            subject=selected_subject,
            quote=form.quote.data,
            quote_author=form.quote_author.data.title(),
            subtitle=form.subtitle.data,
            body=form.message.data,
            img_url=form.image.data,
            author=current_user,
            date=date.today().strftime("%B %e, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template('create.html', form=form, subject_list=all_subjects)


@app.route('/edit/<int:post_id>', methods=['POST', "GET"])
@login_required
def edit_post(post_id):
    all_subjects = db.session.query(Subject).all()
    post = db.session.get(BlogPost, post_id)
    edit_form = BlogForm(
        title=post.title,
        subject=post.subject,
        quote=post.quote,
        quote_author=post.quote_author,
        subtitle=post.subtitle,
        image=post.img_url,
        message=post.body
    )

    edit_form.subject.choices += [(subject.name, subject.name) for subject in all_subjects if
                                  (subject.name, subject.name) not in edit_form.subject.choices]
    edit_form.subject.default = post.subject.name

    if edit_form.validate_on_submit():
        selected_subject = Subject.query.filter_by(name=edit_form.subject.data).first()
        post.title = edit_form.title.data
        post.subject = selected_subject
        post.quote = edit_form.quote.data
        post.quote_author = edit_form.quote_author.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.image.data
        post.body = edit_form.message.data
        db.session.commit()

        return redirect(url_for('blog', post_id=post_id))
    return render_template('edit.html', form=edit_form, post=post)


@app.route('/add-subject', methods=["POST", "GET"])
@login_required
def add_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        if Subject.query.filter_by(name=form.name.data.title()).first():
            flash(message="Person already exists.")
            return redirect(url_for('add_subject'))
        else:
            new_post = Subject(
                name=form.name.data.title(),
                location=form.location.data,
                quote=form.quote.data,
                subtitle=form.subtitle.data,
                birth=form.birth.data,
                death=form.death.data,
                biography=form.message.data,
                img_url=form.image.data,
                visibility=form.visibility.data
            )
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template('add_subject.html', form=form)


@app.route('/delete/<page_type>/<int:post_id>', methods=["POST", "GET"])
@login_required
def delete_post(page_type, post_id):
    if page_type == 'BlogPost':
        db.session.delete(BlogPost.query.filter_by(id=post_id).first())
    elif page_type == 'Subject':
        db.session.delete(Subject.query.filter_by(id=post_id).first())
    db.session.commit()
    return redirect(url_for('home'))


@app.errorhandler(404)
@app.errorhandler(401)
def page_not_found(error):
    format_error = str(error)[0:3]
    error_message = str(error)[str(error).index(":") + 1:]
    return render_template('404.html', error=format_error, error_message=error_message)


@app.route('/elements')
def elements():
    return render_template('elements.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    # if not User.query.all():
    #     new_user1 = User(
    #         name=os.environ.get('USER1'),
    #         password=os.environ.get('PW1')
    #     )
    #     db.session.add(new_user1)
    #
    #     new_user2 = User(
    #         name=os.environ.get('USER2'),
    #         password=os.environ.get('PW2')
    #     )
    #     db.session.add(new_user2)
    #
    #     new_user3 = User(
    #         name=os.environ.get('USER3'),
    #         password=os.environ.get('PW3')
    #     )
    #     db.session.add(new_user3)
    #
    #     new_user4 = User(
    #         name=os.environ.get('USER4'),
    #         password=os.environ.get('PW4')
    #     )
    #     db.session.add(new_user4)
    #     db.session.commit()
    form = LoginForm()
    if form.validate_on_submit():
        new_user1 = User(
            name=form.name.data,
            password=form.password.data
        )
        db.session.add(new_user1)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
