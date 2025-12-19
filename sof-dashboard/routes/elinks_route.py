import os
import sys
from flask import request, Flask, render_template, redirect, session, sessions, url_for, Blueprint
import controller.SecurityController as SecurityController
from models.EvilDomain import EvilDomain
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
@elink_bp.route('evillinks/add', methods=['POST'])
async def add_evil_link():
    if 'id' in session:
        domain = request.form.get('domain')

        try:
            new_domain = EvilDomain(domain)
            db.session.add(new_domain)
            db.session.commit()
        except Exception as e:
            return redirect(url_for('elinks.index'))

        return redirect(url_for('elinks.index'))
    
    return redirect(url_for('auth.login'))

    

