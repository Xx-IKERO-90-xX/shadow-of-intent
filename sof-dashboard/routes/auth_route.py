import os
import sys
from flask import request, Flask, flash, render_template, redirect, session, sessions, url_for, Blueprint
import controller.SecurityController as SecurityController
from models.User import User
from extensions import db

auth_bp = Blueprint('auth', __name__)

# Login route
@auth_bp.route('/auth/login', methods=['GET','POST'])
async def login():
    if session:
        return redirect(url_for('main.index'))
    
    if request.method == 'GET':
        return render_template('/auth/login.jinja')
    else:
        username = request.form['username']
        passwd = request.form['passwd']

        is_verified = await SecurityController.verify_login(username, passwd)

        if is_verified:
            user = db.session.query(User).filter(User.username == username).first()
            session['id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            return redirect(url_for('main.index'))
        else:
            flash("Login fallido!", "error")
            return render_template('/auth/login.jinja')
    
# New admin creation route
@auth_bp.route('/auth/new_admin', methods=['GET','POST'])
async def new_admin():
    if request.method == 'GET':
        return render_template('/auth/new_admin.jinja')
    else:
        passwd = request.form['passwd']
        passwd_repeated = request.form['passwd_repeat']

        if (passwd == passwd_repeated):
            passwd_hashed = await SecurityController.encrypt_passwd(passwd)
            new_admin = User('Administrator', passwd_hashed, 'Admin')
            db.session.add(new_admin)
            db.session.commit()

            return redirect(url_for('auth.login'))
        else:
            error_msg = "Las contraseñas no coinciden."
            return render_template('/auth/new_admin.jinja', error=error_msg)

# Logout route
@auth_bp.route('/auth/logout', methods=['GET'])
async def logout():
    session.clear()
    return redirect(url_for('main.index'))
    