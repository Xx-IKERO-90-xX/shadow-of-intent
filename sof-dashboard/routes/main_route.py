import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
import controller.SecurityController as SecurityController
import controller.UtilsController as UtilsController
from models.EvilDomain import EvilDomain
from models.Repository import Repository
from extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
async def index():
    if 'id' in session:
        total_domain = db.session.query(EvilDomain).count()
        total_repositories = db.session.query(Repository).count()

        formated_domains = UtilsController.format_number(total_domain)
        formated_repositories = UtilsController.format_number(total_repositories)

        return render_template(
            "main/index.jinja",
            total_domain=formated_domains,
            total_repositories=formated_repositories
        )

    if await SecurityController.admin_exists():
        return redirect(url_for('auth.login'))
    return redirect(url_for('auth.new_admin'))