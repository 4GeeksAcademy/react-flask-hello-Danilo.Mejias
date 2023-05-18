"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Favorites
from api.utils import generate_sitemap, APIException

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route("/user", methods=['POST'])
def user_create():
    data=request.get_json()
    print(data)
    new_user=User.query.filter_by(email=data["email"]).first()
    if(new_user is not None):
        return jsonify({
            "msg":"Email registrado"
        }) , 400
    
    print(new_user)
    new_user=User(email=data["email"], password=data["password"], is_active=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize())

@api.route("/user/<int:user_id>", methods=["GET"])
def user_get(user_id):
    user=User.query.get(user_id)
    if(user is None):
        return jsonify({"msg":"Usuario no registrado"}), 404
    
    return jsonify(user.serialize())

#/favorite/1/people/3
@api.route("/favorite/<string:element>/<int:element_id>", methods=['POST'])
def favorite_planet_create(element, element_id):
    user_id=request.get_json()["userId"]
    new_favorite=Favorites(type=element, element_id=element_id, user_id=user_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify({"msg":"Favorite created"}), 201

@api.route("/favorite/<string:element>/<int:element_id>", methods=['DELETE'])
def favorite_planet_delete(element, element_id):
    user_id=request.get_json()["userId"]
    favorite=Favorites.query.filter_by(type=element, element_id=element_id, user_id=user_id).first()

    if(favorite is None):
        return jsonify({"msg":"Favorite not found"}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg":"Favorite delete"}), 200