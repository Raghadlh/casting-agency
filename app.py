import os
from flask import Flask, request, abort, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actor, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    setup_db(app)
    CORS(app, resource={r"/api.*": {"origin": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify({'message': ' Welcom to Casting Agency APP'})

    # GET Actors

    @app.route('/actors', methods=['GET'])
    def actors():
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    # GET Movies
    @app.route('/movies', methods=['GET'])
    def movies():
        movies = Movies.query.all()
        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    # POST Movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(token):
        body = request.get_json()
        new_title = body.get("title", None)
        release_date = body.get("release_date", None)
        try:
            movie = Movies(title=new_title, release_date=release_date)
            movie.insert()

        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    # POST Actor

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actor(token):
        data = request.get_json()
        name = data.get('name', None)
        age = data.get('age', None)
        gender = data.get('gender', None)
        movie_id = data.get('movie_id', None)

        try:
            actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
            actor.insert()
        except Exception:
            abort(422)

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    # PATCH movie

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(token, movie_id):
        body = request.get_json()

        movie = Movies.query.filter(Movies.id == movie_id).first()

        # if the movie is not found
        if movie is None:
            abort(404)

        try:
            title = body.get("title", None)
            release_date = body.get("release_date", None)

            if title:
                movie.title = title

            if release_date:
                movie.release_date = release_date

            movie.update()

            return jsonify({
                "success": True,
                "movie": movie.format()
            }), 200

        except Exception:
            abort(422)

    # PATCH actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(token, actor_id):
        body = request.get_json()

        actor = Actor.query.filter(Actor.id == actor_id).first()

        # if the actor is not found
        if actor is None:
            abort(404)

        try:
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            movie_id = body.get('movie_id', None)

            if name:
                actor.name = name

            if age:
                actor.age = age

            if gender:
                actor.gender = gender

            if movie_id:
                actor.movie_id = movie_id

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

        except Exception:
            abort(422)

    # DELETE movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):
        movie = Movies.query.filter(Movies.id == movie_id).first()

        # if the movie is not found
        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie.id
            }), 200

        except Exception:
            abort(422)

    # DELETE actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).first()

        # if the actor is not found
        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actor.id
            }), 200

        except Exception:
            abort(422)

    # Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
