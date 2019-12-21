from flask import url_for, redirect, request, render_template, flash

from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import ActionsMixin
from flask_admin import BaseView, expose, AdminIndexView
from flask_admin.form import rules

from .models import User, CKTextAreaField
from . import bcrypt

from flask_login import current_user

from wtforms import PasswordField


# , StringField,  SubmitField, BooleanField, TextAreaField, widgets #ed


class HelloView(BaseView):
    @expose('/')
    def index(self):
        return self.render('some-template.html')


class UserAdminView(ModelView, ActionsMixin):
    column_searchable_list = ('username',)
    column_sortable_list = ('username', 'admin')
    column_exclude_list = ('password',)
    form_excluded_columns = ('password',)

    # form_edit_rules = ('username', 'admin',)
    form_edit_rules = (rules.Header('Edit info for:'), 'username', 'admin', 'notes',
                       rules.Header('Reset Password'), 'new_password', 'confirm')
    # form_create_rules = ('username', 'admin', 'email', 'notes', 'password')

    form_create_rules = (
        rules.FieldSet(('username', 'notes', 'email'), 'Personal'),
        rules.FieldSet(('admin', 'password'), 'Permission'),
    )

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin()

    def inaccessible_callback(self, name, *kwargs):
        return redirect(url_for('home', next=request.url))

    def scaffold_form(self):
        form_class = super(UserAdminView, self).scaffold_form()
        form_class.password = PasswordField('Password')
        form_class.new_password = PasswordField('New Password')
        form_class.confirm = PasswordField('Confirm_ New Password')
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

    form_overrides = dict(notes=CKTextAreaField)
    create_template = 'edit.html'
    edit_template = 'edit.html'

    def update_model(self, form, model):
        form.populate_obj(model)
        if form.new_password.data:
            if form.new_password.data != form.confirm.data:
                flash('Passwords must match!!!')
                return
            model.password = bcrypt.generate_password_hash(form.new_password.data)
        self.session.add(model)
        self._on_model_change(form, model, False)
        self.session.commit()


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('home', next=request.url))