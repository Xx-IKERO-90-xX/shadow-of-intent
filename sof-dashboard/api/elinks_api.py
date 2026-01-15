from flask import request, jsonify, Blueprint
from extensions import db
from models.EvilDomain import EvilDomain

elinks_api = Blueprint("elinks_api", __name__, url_prefix="/api/elinks")

@elinks_api.route("/", methods=["GET"])
def get_evil_links():
    evil_links = db.session.query(EvilDomain).all()
    return jsonify(evil_links)

@elinks_api.route('/<int:id>', methods=["GET"])
def get_link_by_id(id):
    evil_link = EvilDomain.query.get(id)

    if not evil_link:
        return jsonify({"error": "Evil link don't exists."}), 404
    
    return jsonify(evil_link.to_dict())