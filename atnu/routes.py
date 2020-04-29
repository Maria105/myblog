from flask import render_template, url_for, flash, redirect, request, abort, json, jsonify, make_response
from atnu import app, db, bcrypt
from atnu.forms import RegistrationForm, LoginForm, PersonForm, AdminUserCreateForm, AdminUserUpdateForm #, UserAdminView
from atnu.models import User, Person
from flask_login import login_user, current_user, logout_user, login_required
import os
import secrets
from PIL import Image
from datetime import datetime
from functools import wraps
import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from functools import wraps


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise




@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
#    persons = Person.query.order_by(Person.date_posted.desc()).paginate(page=page, per_page=5)
 #   return render_template('home.html', posts=posts)





@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


"""@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        if bcrypt.check_password_hash(current_user.password, form.old_pass.data):
            hashed_password = bcrypt.generate_password_hash(form.new_pass.data).decode('utf-8')
            current_user.password = hashed_password
        else:
            flash('Old password is wrong!', 'danger')
            return redirect('account')
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)
"""

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
#    page = request.args.get('page', 1, type=int)
#    posts = Post.query.filter_by(user_id=user.id).paginate(page, 20, False)
    return render_template('user.html', user=user) #posts=posts.items)



@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['email'] = user.email
        if type(user.password) == str:
            user_data['password'] = user.password
        else:
            user_data['password'] = user.password.decode('utf-8')
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/users/<id>', methods=['GET'])
def get_one_user(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    user_data = {'username': user.username, 'email': user.email, 'password': user.password,
                 'admin': user.admin}
    return jsonify({'user': user_data})


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(data['password'])

    new_user = User(username=data['username'], email=data['email'],
                    password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created'})


@app.route('/users/<id>', methods=['PUT'])
def promote_user(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted'})


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found'})

    db.session.delete(user)
    db.session.commit()
    return jsonify({'users': 'The user has been deleted'})

@ app.route("/person/new", methods=['GET', 'POST'])
@login_required
def new_person():
    form = PersonForm()
    if form.validate_on_submit():
        person = Person(name=form.name.data, email=form.email.data, bday=form.bday.data, residence=form.residence.data, work_place=form.work_place.data, position=form.position.data, degree=form.degree.data, academic_status=form.academic_status.data, scientific_specialty=form.scientific_specialty.data, phone=form.phone.data, status=form.status.data, id_number=form.id_number.data, solution_number=form.solution_number.data, date_of_decision=form.date_of_decision.data)
        db.session.add(person)
        db.session.commit()
#        flash('Ви додали нового користувача!', 'saccess')
        return redirect(url_for('home'))
    return render_template('add_person.html', title='new person', form=form, legend='New Person')



@app.route("/person/<int:person_id>/update", methods=['GET', 'POST'])
@login_required
def update_person(person_id):
    person = Person.query.get_or_404(person_id)
    if person.author != current_user:
        abort(403)
    form = PersonForm()
    if form.validate_on_submit():
        person.name = form.name.data
        person.email = form.email.data
        person.bday = form.bday.data
        person.residence=form.residence.data
        person.work_place=form.work_place.data
        person.position=form.position.data
        person.degree=form.degree.data
        person.academic_status=form.academic_status.data
        person.scientific_specialty=form.scientific_specialty.data
        person.phone=form.phone.data
        person.status=form.status.data
        person.id_number=form.id_number.data
        person.solution_number=form.solution_number.data
        person.date_of_decision=form.date_of_decision.data

        db.session.commit()
        flash('Person has been updated!', 'success')
        return redirect(url_for('person', person_id=person.id))
    elif request.method == 'GET':
        form.name.data = person.name
        form.email.data = person.email
        form.bday.data = person.bday
        form.residence.data = person.residence
        form.work_place.data = person.work_place
        form.position.data = person.position
        form.degree.data = person.degree
        form.academic_status.data = person.academic_status
        form.scientific_specialty.data = person.scientific_specialty
        form.phone.data = person.phone
        form.status.data = person.status 
        form.id_number.data = person.id_number
        form.solution_number.data = person.solution_number
        form.date_of_decision.data = person.date_of_decision
    return render_template('add_person.html', title='Update Person', person_id=person_id, legend='Update Person')

"""@app.route("/person/<int:person_id>", methods=['GET','POST'])
def person(person_id):
    if request.method == 'POST':
        comment = Comment(body=request.form.get('body'), person_id=person_id, user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added to the post", "success")
    post = Post.query.get_or_404(post_id)
  #  comments = []
    comments = Comment.query.filter_by(post_id=post_id)
    return render_template('post.html',title=post.title, post=post, comments=comments)
"""
@app.route("/person/<int:person_id>/delete", methods=['POST'])
@login_required
def delete_person(person_id):
    person = Person.query.get_or_404(person_id)
#    if post.author != current_user:
#        abort(403)
    db.session.delete(person)
    db.session.commit()
    flash('Your person has been deleted!', 'success')
    return render_template('add_person.html', title='Delete Person', person_id=person_id, legend='Delete Person')




"""
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
"""




def admin_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin():
            return abort(403)
        return func(*args, **kwargs)

    return decorated_view


@app.route('/admin')
@login_required
@admin_login_required
def home_admin():
    return render_template('admin-home.html')


@app.route('/admin/users-list')
@login_required
@admin_login_required
def users_list_admin():
    users = User.query.all()
    return render_template('users-list-admin.html', users=users)


@app.route('/admin/create-user', methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_create_admin():
    form = AdminUserCreateForm(request.form)
    if form.validate():
        username = form.username.data
        password = form.password.data
        admin = form.admin.data
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash('This username has been already taken. Try another one.', 'warning')
            return render_template('register.html', form=form)
        user = User(username, password, admin)
        db.session.add(user)
        db.session.commit()
        flash('New User Created.', 'info')
        return redirect(url_for('users_list_admin'))
        if form.errors:
            flash(form.errors, 'danger')
        return render_template('user-create-admin.html', form=form)


@app.route('/admin/update-user/<id>', methods=['GET', 'POST'])
@login_required
@admin_login_required
def user_update_admin(id):
    user = User.query.get(id)
    form = AdminUserUpdateForm(
        request.form,
        username=user.username,
        admin=user.admin)
    if form.validate():
        username = form.username.data
        admin = form.admin.data

        User.query.filter_by(id=id).update({
            'username': username,
            'admin': admin, })
        db.session.commit()
        flash('User Updated.', 'info')
        return redirect(url_for('users_list_admin'))
        if form.errors:
            flash(form.errors, 'danger')
            return render_template('user-update-admin.html', form=form, user=user)


@app.route('/admin/dalete-user/<id>')
@login_required
@admin_login_required
def user_delete_admin(id):
    user = User.query.get(id)
    user.delete()
    db.session.commit()
    flash('User Deleted.')
    return redirect(url_for('users_list_admin'))


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():
        return redirect((url_for('search_results', query=form.search.data)))  # or what you want
    return render_template('home.html', form=form)

@app.route('/search_results/<query>')
@login_required
def search_results(query):
  results = User.query.whoosh_search(query).all()
  return render_template('search_results.html', query=query, results=results)


