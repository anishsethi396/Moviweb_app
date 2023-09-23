# api.py
from flask import Blueprint, jsonify
from flask import Flask, render_template, url_for, request, redirect
from Moviweb_app.models.data_models import db
from data_manager.sqlite_data_manager import SQLiteDataManager

api = Blueprint('api', __name__)

data_manager = SQLiteDataManager(db)


@api.route('/users', methods=['GET'])
def list_users():
    """
    Handle requests to the '/users' route and render the 'users.html' template
    """
    users = data_manager.get_all_users()
    return render_template("users.html", users=users)


@api.route('/users/<int:user_id>')
def get_user_movies(user_id):
    """
    Retrieve and display a list of movies for a specific user.
    """
    user_movie = data_manager.get_user_movie(user_id)
    user_name = data_manager.get_user_name(user_id)
    return render_template('user_movies.html', user_movie=user_movie, user_name=user_name, user_id=user_id)


@api.route('/users/add_movie/<int:user_id>', methods=['GET', 'POST'])
def add_movie(user_id):
    """
    Handles the addition of a movie for a specific user.
    """
    if request.method == 'POST':
        movie = request.form.get('movie')
        movie_data = data_manager.movies_api(movie)
        if movie_data is None:
            return redirect('404.html')
        else:
            data_manager.add_movie_for_user(user_id, movie_data)
            return redirect(url_for('api.get_user_movies', user_id=user_id, movie_data=movie_data))
    return render_template('add_movie.html', user_id=user_id)
