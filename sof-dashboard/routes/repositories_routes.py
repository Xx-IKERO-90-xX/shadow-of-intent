import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
import controller.SecurityController as SecurityController
from models.Repository import Repository
import re
from extensions import db

JSON_REGEX  = r'^https?:\/\/([a-zA-Z0-9]([a-zA-Z0-9\-].*[a-zA-Z0-9])?\.)+[a-zA-Z](\/[^\s]*)*\/?[^\s]*\.json$'
TXT_REGEX   = r'^https?:\/\/([a-zA-Z0-9]([a-zA-Z0-9\-].*[a-zA-Z0-9])?\.)+[a-zA-Z](\/[^\s]*)*\/?[^\s]*\.txt$'

repo_bp = Blueprint('repo', __name__)

# Rutas para la gestión de repositorios externos
@repo_bp.route('/repositories', methods=['GET'])
async def index():
    if 'id' in session:
        page = request.args.get('page', 1, type=int)
        pagination = Repository.query.paginate(page=page, per_page=10)
        repositories = pagination.items

        return render_template("repositories/index.jinja", repositories=repositories, pagination=pagination)
    
    return redirect(url_for('auth.login'))

# Esta ruta maneja la adición de un nuevo repositorio externo
@repo_bp.route('/repositories/add', methods=['POST'])
async def add_repository():
    if 'id' in session:
        name = request.form.get('name')
        url = request.form.get('url')
        description = request.form.get('description')
        type = request.form.get('type')

        if type == 'json':
            if not re.match(JSON_REGEX, url):
                return redirect(url_for('repo.index'))
            
            new_repo = (name, url, description, type)
            db.session.add(new_repo)
            db.session.commit()

        elif type == 'txt':
            if not re.match(TXT_REGEX, url):
                return redirect(url_for('repo.index'))
            
            new_repo = Repository(name, url, description, type)
            db.session.add(new_repo)
            db.session.commit()
        
        else:
            return redirect(url_for('repo.index'))

        return redirect(url_for('repo.index'))

    return redirect(url_for('repo.index'))