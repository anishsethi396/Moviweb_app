import requests
from .data_manager_interface import DataManagerInterface
from Moviweb_app.models.data_models import User, Movie, Review

API_KEY = 79153533


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db):
        """
        Initialize a new instance of SQLiteDataManager class.
        :param db:
        """
        self.db = db

    def get_all_users(self):
        """
        Retrieve a list of all the Users from the Database.
        :return:
        """
        try:
            return User.query.all()
        except Exception as e:
            print(f"Error retrieving users from the database: {e}")
            return []

    def get_user_movie(self, user_id):
        """
        Retrieve a list of movies for a specific User
        :param user_id:
        :return:
        """
        try:
            movies = self.db.session.query(Movie).filter(Movie.user_id == user_id).all()
            return movies
        except Exception as e:
            print(f"Error retrieving movies for user from the database: {e}")
            return []

    def add_user(self, new_user):
        """
        Add a new user in the database
        :param new_user:
        :return:
        """
        try:
            self.db.session.add(new_user)
            self.db.session.commit()
            return True
        except Exception as e:
            print(f"Error adding a new user to the database: {e}")
            return False

    def delete_user(self, user_id):
        """
        Delete a user from the database
        :param user_id:
        :return:
        """
        try:
            user = self.db.session.query(User).filter(User.id == user_id).first()
            if user:
                self.db.session.delete(user)
                self.db.session.commit()
        except Exception as e:
            print(f"Error deleting user from the database: {e}")

    def update_user(self, user_id, new_name):
        """
        Update user's name in the Database
        :param user_id:
        :param new_name:
        :return:
        """
        try:
            user = self.db.session.query(User).filter(User.id == user_id).first()
            if user:
                user.name = new_name
                self.db.session.commit()
        except Exception as e:
            print(f"Error updating user in the database: {e}")

    @staticmethod
    def create_user_details(user_id, user_name):
        """
        Creates a new User object with the provided user_id and User_name
        :param user_id:
        :param user_name:
        :return:
        """
        new_user = User(id=user_id, name=user_name)
        return new_user

    def get_user_name(self, user_id):
        """
        Retrieve the name of a User by the user_id from the Database
        :param user_id:
        :return:
        """
        try:
            user = self.db.session.query(User).filter(User.id == user_id).first()
            if user:
                return user.name
            else:
                return None
        except Exception as e:
            print(f"Error retrieving user name from the database: {e}")

    @staticmethod
    def generate_user_id(users):
        """
        This function is only intended for the app to work smoothly with other databases.
        :param users:
        :return:
        """
        return None

    @staticmethod
    def generate_movie_id(self, user_id):
        """
        This function is only intended for the app to work smoothly with other databases.
        :param self:
        :param user_id:
        :return:
        """
        return None

    def add_movie_for_user(self, user_id, new_movie):
        """
        Add a new movie for a user in the database.
        """

        try:
            movie = Movie(
                user_id=user_id,
                title=new_movie['title'],
                director=new_movie['director'],
                year=new_movie['year'],
                rating=new_movie['rating'],
                poster=new_movie['poster']
            )
            self.db.session.add(movie)
            self.db.session.commit()
        except Exception as e:
            print(f"Error adding a new movie for the user: {e}")

    def update_movie(self, user_id, movie_id, new_title, new_director, new_year, new_rating):
        """
        Update user's movie information in the database.
        """
        try:
            movie = self.db.session.query(Movie).filter(Movie.user_id == user_id, Movie.movie_id == movie_id).first()
            if movie:
                movie.title = new_title
                movie.director = new_director
                movie.year = new_year
                movie.rating = new_rating
                self.db.session.commit()
        except Exception as e:
            print(f"Error updating movie in the database: {e}")

    def delete_movie(self, user_id, movie_id):
        """
        Delete a specific movie for a user from the Database
        """
        try:
            movie = self.db.session.query(Movie).filter(Movie.user_id == user_id, Movie.movie_id == movie_id).first()
            if movie:
                self.db.session.delete(movie)
                self.db.session.commit()
        except Exception as e:
            print(f"Error deleting movie from the database: {e}")

    def get_movie_by_id(self, user_id, movie_id):
        """
         Retrieve a specific movie from a user's movie database by the movie ID.
        """
        try:
            movie = self.db.session.query(Movie).filter(Movie.user_id == user_id, Movie.movie_id == movie_id).first()
            if movie:
                movie_info = {
                    "title": movie.title,
                    "director": movie.director,
                    "year": movie.year,
                    "rating": movie.rating,
                    "poster": movie.poster,
                    "movie_id": movie.movie_id
                }
                return movie_info
            else:
                return None
        except Exception as e:
            print(f"Error retrieving movie from the database: {e}")

    @staticmethod
    def movies_api(new_movie):
        """
        Fetch the movie information from the OMDB api using the movie title
        :param new_movie:
        :return:
        """
        api_url = f'http://www.omdbapi.com/?apikey={API_KEY}&t={new_movie}'
        try:
            response = requests.get(api_url)
            api_data = response.json()
            if api_data['Response'] == "False":
                return None
            else:
                movie_info = {
                    "title": api_data["Title"],
                    "year": api_data["Year"],
                    "director": api_data["Director"],
                    "rating": api_data["imdbRating"],
                    "poster": api_data["Poster"]
                }
                return movie_info
        except Exception as error:
            print(f"{error}\n Check connections!")
            return None

    def add_review(self, user_id, movie_id, review):
        """
        Gets new user details data and returns a review of user
        """
        review_to_add = Review(user_id=user_id, movie_id=movie_id, review=review)
        self.db.session.add(review_to_add)
        self.db.session.commit()
        return review_to_add

    def get_reviews(self, user_id, movie_id):
        """
        Get all reviews for a specific movie associated with a user.
        """
        reviews = self.db.session.query(Review).filter(
            Review.movie_id == movie_id,
            Review.user_id == user_id
        ).all()

        if reviews:
            return reviews

    def delete_review(self, user_id, movie_id, review_id):
        """
        Deletes a review from database
        """
        self.db.session.query(Review).filter(
            Review.movie_id == movie_id,
            Review.user_id == user_id,
            Review.review_id == review_id
        ).delete()
        self.db.session.commit()
