import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint, flash
import controller.SecurityController as SecurityController
import controller.EvilLinksController as EvilLinksController
from models.EvilDomain import EvilDomain
from models.Repository import Repository
from extensions import db

elink_bp = Blueprint('elinks', __name__)

# Rutas para la gestión de enlaces maliciosos
@elink_bp.route('/evillinks', methods=['GET'])
async def index():
    if 'id' in session:
        page = request.args.get('page', 1, type=int)
        evillinks = EvilDomain.query.paginate(
            page=page,
            per_page=5,
            error_out=False
        )

        total_links = db.session.query(EvilDomain).count()

        return render_template(
            "evillinks/index.jinja", 
            evillinks=evillinks, 
            total_links=total_links
        )
    
    return redirect(url_for('auth.login'))

# Esta ruta maneja la adición de un nuevo enlace malicioso
@elink_bp.route('/evillinks/add', methods=['POST'])
async def add_evil_link():
    if 'id' in session:
        domain = request.form.get('domain')

        try:
            new_domain = EvilDomain(domain)
            db.session.add(new_domain)
            db.session.commit()
            flash("Se ha creado la fuente externa de manera exitosa!!", "success")
        except Exception as e:
            flash("El enlace malicioso ya existe!!", "error")
        
        return redirect(url_for('elinks.index'))
    
    return redirect(url_for('auth.login'))

# Esta ruta maneja la eliminación de un enlace malicioso
@elink_bp.route('/evillinks/delete/<int:id>', methods=['GET'])
async def delete_evil_link(id):
    if 'id' in session:
        evil_link = EvilDomain.query.get_or_404(id)

        try:
            db.session.delete(evil_link)
            db.session.commit()

            flash("Enlace malicioso eliminado!!", "success")
        except Exception as e:
            flash("Error en la eliminación del enlace malicioso!!", "error")
        return redirect(url_for('elinks.index'))

    return redirect(url_for('auth.login'))


@elink_bp.route('/evillinks/reload', methods=['GET'])
async def reload_evil_domains():
    if 'id' in session:
        repositories = Repository.query.all()
        for repo in repositories:
            if repo.type == 'json':
                await EvilLinksController.extract_from_JSON_repository(repo)

            if repo.type == 'txt':
                await EvilLinksController.extract_from_TXT_repository(repo)
        
        return redirect(url_for('elinks.index'))

    return redirect(url_for('auth.login'))
