from flask import Flask, render_template, url_for, request, redirect
from data_manager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('data/data.json')


@app.route('/')
def home():
    """
    Render the home page template
    """
    return render_template("home.html")


@app.route('/users')
def list_users():
    """
    Handle requests to the '/users' route and render the 'users.html' template
    """
    users = data_manager.get_all_users()
    return render_template("users.html", users=users)


@app.route('/users/<int:user_id>')
def get_user_movies(user_id):
    """
    Retrieve and display a list of movies for a specific user.
    """
    user_movie = data_manager.get_user_movie(user_id)
    user_name = data_manager.get_user_name(user_id)
    return render_template('user_movies.html', user_movie=user_movie, user_name=user_name, user_id=user_id)


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
        return redirect(url_for('list_users'))
    return render_template('add_users.html')


@app.route('/users/delete_users/<int:user_id>')
def delete_user(user_id):
    """
    Handles the deletion of a user with the given user_id.
    """

    data_manager.delete_user(user_id)
    return redirect(url_for('list_users'))


@app.route('/users/update_users/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    if request.method == 'POST':
        new_name = request.form.get('name')
        data_manager.update_user(user_id, new_name)
        return redirect(url_for('list_users'))
    return render_template('update_user.html', user_id=user_id)


@app.route('/users/add_movie/<int:user_id>', methods=['GET', 'POST'])
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
            movie_id = data_manager.generate_movie_id(user_id)
            data_manager.add_movie_for_user(user_id, movie_id, movie_data)
            return redirect(url_for('get_user_movies', user_id=user_id, movie_data=movie_data))
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/delete_movie/<int:user_id>/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """
    Handles the deletion of a movie for a specific user.
    """
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for('get_user_movies', user_id=user_id))


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
        return redirect(url_for('get_user_movies', user_id=user_id))

    movie = data_manager.get_movie_by_id(user_id, movie_id)
    return render_template('update_movie.html', user_id=user_id, movie=movie)


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
    app.run(debug=True, port=5000)
