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
        repositories = Repository.query.paginate(
            page=page,
            per_page=5,
            error_out=False
        )

        return render_template("repositories/index.jinja", repositories=repositories)
    
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
            
            if description is None:
                description = ""
            
            new_repo = Repository(name, url, description, type)
            db.session.add(new_repo)
            db.session.commit()

        elif type == 'txt':
            if not re.match(TXT_REGEX, url):
                return redirect(url_for('repo.index'))
            
            if description is None:
                description = ""
            
            new_repo = Repository(name, url, description, type)
            db.session.add(new_repo)
            db.session.commit()
        
        else:
            return redirect(url_for('repo.index'))

        return redirect(url_for('repo.index'))

    return redirect(url_for('repo.index'))

# Esta ruta maneja la eliminación de un repositorio externo
@repo_bp.route('/repositories/delete/<int:id>', methods=['GET'])
async def delete_repository(id):
    if 'id' in session:
        repo = Repository.query.get(id)
        if repo:
            db.session.delete(repo)
            db.session.commit()
        
        return redirect(url_for('repo.index'))
    
    return redirect(url_for('auth.login'))

# Esta ruta maneja la edición de la descripción de un repositorio externo
@repo_bp.route('/repositories/edit/description/<int:id>', methods=['POST'])
async def edit_description(id):
    if 'id' in session:
        repo = Repository.query.get(id)
        if repo:
            new_description = request.form.get('description')
            repo.description = new_description
            db.session.commit()
        
        return redirect(url_for('repo.index'))
    
    return redirect(url_for('auth.login'))

