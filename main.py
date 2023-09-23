from flask import Flask, render_template, url_for, request, redirect
from Moviweb_app.models.data_models import db
from data_manager.sqlite_data_manager import SQLiteDataManager
from api import api

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')  # Registering the blueprint
app.config[
    'SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\15879\PycharmProjects\moviweb_app\Moviweb_app\data\data.sqlite3'
db.init_app(app)

# While using JSON database
# data_manager = JSONDataManager('data/data.json')

# While using SQlite database
data_manager = SQLiteDataManager(db)


@app.route('/')
def home():
    """
    Render the home page template
    """
    return render_template("home.html")


@app.route('/users/add_users', methods=['GET', 'POST'])
def add_users():
    """
    Handles the addition of new users.
    """
    users = data_manager.get_all_users()
    if request.method == 'POST':
        name = request.form.get("name")
        new_user_id = data_manager.generate_user_id(users)
        new_user = data_manager.create_user_details(new_user_id, name)

        data_manager.add_user(new_user)
        return redirect(url_for('api.list_users'))
    return render_template('add_users.html')


@app.route('/users/delete_users/<int:user_id>')
def delete_user(user_id):
    """
    Handles the deletion of a user with the given user_id.
    """

    data_manager.delete_user(user_id)
    return redirect(url_for('api.list_users'))


@app.route('/users/update_users/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'POST':
        new_name = request.form.get('name')
        data_manager.update_user(user_id, new_name)
        return redirect(url_for('api.list_users'))
    return render_template('update_user.html', user_id=user_id)


@app.route('/users/delete_movie/<int:user_id>/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """
    Handles the deletion of a movie for a specific user.
    """
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('api.get_user_movies', user_id=user_id))


@app.route('/users/update_movie/<int:user_id>/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
    Handle updating a movie's details for a specific user.
    """
    if request.method == 'POST':
        new_title = request.form['title']
        new_director = request.form['director']
        new_year = request.form['year']
        new_rating = request.form['rating']
        data_manager.update_movie(user_id, movie_id, new_title, new_director, new_year, new_rating)
        return redirect(url_for('api.get_user_movies', user_id=user_id))

    movie = data_manager.get_movie_by_id(user_id, movie_id)
    return render_template('update_movie.html', user_id=user_id, movie=movie)


@app.route('/users/<int:user_id>/add_review/<int:movie_id>', methods=['GET', 'POST'])
def add_review(user_id, movie_id):
    """
    route function to adding a review
    :param user_id:
    :param movie_id:
    :return:
    """
    if request.method == 'POST':
        review = request.form.get('review')

        data_manager.add_review(user_id, movie_id, review)

        return redirect(url_for('api.get_user_movies', user_id=user_id))

    return render_template('add_review.html', user_id=user_id, movie_id=movie_id)


@app.route('/users/<int:user_id>/see_reviews/<int:movie_id>', methods=['GET'])
def view_reviews(user_id, movie_id):
    """
    route function to see all reviews of a movie
    :param user_id:
    :param movie_id:
    :return:
    """
    reviews = data_manager.get_reviews(user_id, movie_id)
    return render_template('view_reviews.html',
                           user_id=user_id,
                           movie_id=movie_id, reviews=reviews)


@app.route('/users/<int:user_id>/delete_review/<int:movie_id>/<int:review_id>', methods=['GET'])
def delete_review(user_id, movie_id, review_id):
    """
    route function to delete a review
    :param user_id:
    :param movie_id:
    :param review_id:
    :return:
    """
    data_manager.delete_review(user_id, movie_id, review_id)  # Delete the review from the database
    return redirect(url_for('view_reviews', user_id=user_id, movie_id=movie_id))


@app.errorhandler(404)
def page_not_found(error):
    """
    route function to "page not found" page.
    :params: user_id, movie_id
    :return: 404.html template
    """
    return render_template('404.html', error=error), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    route function to "internal server error" page.
    :params: user_id, movie_id
    :return: 500.html template
    """
    return render_template('500.html', error=error), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
