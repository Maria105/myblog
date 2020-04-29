from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from atnu.models import User, CKTextAreaField
#from flask_ckeditor import CKEditor, CKEditorField
#from flask_admin import BaseView, expose
#from flask_admin.contrib.sqla import ModelView
#from flask_admin.actions import ActionsMixin
#from flask_admin.form import rules
from atnu import bcrypt


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
	submit = SubmitField('Sign up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if False:
			raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError('Email already registered.')


class LoginForm(FlaskForm): 
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')	


"""class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	about_me = TextAreaField('About Me')
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) 
	old_pass = PasswordField('Old password', validators=[DataRequired()])
	new_pass = PasswordField('New password', validators=[DataRequired()])
	confirm_pass = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('new_pass')])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('That email is taken. Please choose a different one.')
"""
class PersonForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	email = StringField('E-mail', validators=[DataRequired()])
	bday = DateTimeField('Birthday', format='%Y-%m-%d', validators=[DataRequired()])
	residence = StringField('Residence', validators=[DataRequired()])
	work_place = StringField('Work place', validators=[DataRequired()])
	position = TextAreaField('Position', validators=[DataRequired()])
	degree = StringField('Degree', validators=[DataRequired()])
	academic_status = StringField('Academic statuc', validators=[DataRequired()])
	scientific_specialty = StringField('Scientific specialty', validators=[DataRequired()])
	phone = StringField('Phone', validators=[DataRequired()])	
	status = StringField('Status', validators=[DataRequired()])
	id_number = StringField('ID number', validators=[DataRequired()])
	solution_number = StringField('Solution number', validators=[DataRequired()])	
	date_of_decision = DateTimeField('Data of decision', format='%Y-%m-%d', validators=[DataRequired()])
	submit = SubmitField('Post')


class AdminUserCreateForm(FlaskForm):
	username = StringField('Username', [DataRequired()])
	password = PasswordField('Password', [DataRequired()])
	admin = BooleanField('Is Admin ?')

class AdminUserUpdateForm(FlaskForm):
	username = StringField('Username', [DataRequired()])
	admin = BooleanField('Is Admin ?')

""" ***class UserAdminView(ModelView, ActionsMixin):
    column_searchable_list = ('username',)
    column_sortable_list = ('username', 'admin')
    column_exclude_list = ('password',)
    form_excluded_columns = ('password',)
    form_edit_rules = ('username', 'admin',)
  
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def scaffold_form(self):
    	form_class = super(UserAdminView, self).scaffold_form()
    	form_class.password = PasswordField('Password')
    	form_class.new_password = PasswordField('New Password')
    	form_class.confirm = PasswordField('Confirm New Password')
    	return form_class

    def create_model(self, form):
        model = self.model(
            form.username.data, form.password.data, form.admin.data
        )
        form.populate_obj(model)
        model.password = bcrypt.generate_password_hash(form.password.data)
        self.session.add(model)
        self._on_model_change(form, model, True)
        self.session.commit()

    form_edit_rules = ('username', 'admin', 'notes', rules.Header('Reset Password'),'new_password', 'confirm')
    form_create_rules = ('username', 'admin', 'email', 'notes', 'password')

    form_overrides = dict(notes=CKTextAreaField)
    create_template = 'edit.html'
    edit_template = 'edit.html'

    def update_model(self, form, model):
    	form.populate_obj(model)
    	if form.new_password.data:
    		if form.new_password.data != form.confirm.data:
    			flash('Passwords must match')
    			return
    		model.password = bcrypt.generate_password_hash(form.new_password.data)
    	self.session.add(model)
    	self._on_model_change(form, model, False)
    	self.session.commit()
"""
#class AddCommentForm(FlaskForm):
#	body = StringField("Body", validators=[DataRequired()])
#	submit = SubmitField("Post")

class SearchForm(Form):
  search = StringField('search', [DataRequired()])
  submit = SubmitField('Search', render_kw={'class': 'btn btn-success btn-block'})