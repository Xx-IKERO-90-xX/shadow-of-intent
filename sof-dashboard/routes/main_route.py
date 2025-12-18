import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
import controller.SecurityController as SecurityController

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
async def index():
    if 'id' in session:
        return render_template("main/index.jinja")

    if await SecurityController.admin_exists():
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.new_admin'))