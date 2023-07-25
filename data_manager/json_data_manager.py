import json
import requests
from .data_manager_interface import DataManagerInterface

API_KEY = 79153533


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        """
        Initialize a new instance of the JSONDataManager class
        :param filename:
        """

        self.filename = filename

    def get_all_users(self):
        # Return all the users all users
        with open(self.filename) as fileobj:
            data = json.loads(fileobj.read())
            return data

    def get_user_movie(self, user_id):
        # Return all the movies for a given user
        try:
            all_users = self.get_all_users()
            for user in all_users:
                if user['id'] == user_id:
                    return user['movies']
            return None
        except Exception as error:
            return error

    def update_json(self, new_file):
        """
        Update the JSON data file with new content.
        :param new_file: A dictionary containing the updated data.
        :return:
        """
        try:
            with open(self.filename, "w") as fileobj:
                fileobj.write(json.dumps(new_file, indent=4))
        except IOError as error:
            print("An IOError occurred: ", str(error))

    def create_user_details(self, user_id, user_name):
        """
        Create a new user details dictionary
        :param user_id: The unique ID for the user
        :param user_name: The name of the user
        :return: A new dictionary containing the users details in a specific format.
        """
        new_user = {
            "id": user_id,
            "name": user_name,
            "movies": [
                {
                    "movie_id": self.generate_movie_id(user_id),
                    "title": "Add movies here: "
                }
            ]
        }
        return new_user

    def add_user(self, new_user):
        """
        Add a new user to the existing lists of users.
        :param new_user: A dictionary representing the details of a new user.
        :return: The updated list of all users.
        """
        all_users = self.get_all_users()
        all_users.append(new_user)
        self.update_json(all_users)
        return all_users

    def delete_user(self, user_id):
        """
        Delete a user with the given user_id from the list of all users.
        """
        all_users = self.get_all_users()
        updated_list = []
        user_to_remove = None
        for user in all_users:
            if user['id'] != user_id:
                updated_list.append(user)
            else:
                user_to_remove = user
        self.update_json(updated_list)
        return user_to_remove

    def update_user(self, user_id, new_name):
        """
        Update the name of the user with the given user_id
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user['id'] == user_id:
                user['name'] = new_name
                self.update_json(all_users)
                return user
        return None

    def get_user_name(self, user_id):
        """
        Get the name of the user with the given user_id
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user['id'] == user_id:
                return user['name']
        return None

    @staticmethod
    def generate_user_id(users):
        """
        Generate a uniques user_id for a new user
        """
        if not users:
            return 1
        return max([user['id'] for user in users]) + 1

    def generate_movie_id(self, user_id):
        """
        Generate a unique movie_id for a new movie associated with the given user.
        """
        user_movie = self.get_user_movie(user_id)
        if not user_movie:
            return 1
        return max([movie['movie_id'] for movie in user_movie]) + 1

    def get_movie_by_id(self, user_id, movie_id):
        """
        Retrieve a specific movie from a user's movie list using its movie_id
        """
        movies = self.get_user_movie(user_id)
        for movie in movies:
            if movie['movie_id'] == movie_id:
                return movie
        return None

    @staticmethod
    def movies_api(new_movie):
        """
        Fetch movie information from the OMDB API using the movie title.
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

    def add_movie_for_user(self, user_id, movie_id, new_movie):
        """
        Add a new movie to the user's movie list.
        """

        all_users = self.get_all_users()
        for user in all_users:
            if user['id'] == user_id:
                user['movies'].append({
                    "movie_id": movie_id,
                    "title": new_movie['title'],
                    "director": new_movie['director'],
                    "year": new_movie['year'],
                    "rating": new_movie['rating'],
                    "poster": new_movie['poster']
                })
                self.update_json(all_users)
                return

    def update_movies_data(self, user_id, movie_list):
        """
        Update the movie list for a specific user in the list of all the users.
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user['id'] == user_id:
                user['movies'] = movie_list
        self.update_json(all_users)
        return movie_list

    def delete_movie(self, user_id, movie_id):
        """
        Delete a specific movie from a user's movie list.
        """
        user_movies = self.get_user_movie(user_id)
        updated_list = []
        movie_to_delete = None
        for movie in user_movies:
            if movie['movie_id'] != movie_id:
                updated_list.append(movie)
            else:
                movie_to_delete = movie
        self.update_movies_data(user_id, updated_list)
        return movie_to_delete

    def update_movie(self, user_id, movie_id, new_title, new_director, new_year, new_rating):
        """
        Update details of a specific movie for a user in the list of all users.
        """
        all_users = self.get_all_users()
        for user in all_users:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['movie_id'] == movie_id:
                        movie['title'] = new_title
                        movie['director'] = new_director
                        movie['year'] = new_year
                        movie['rating'] = new_rating
        self.update_json(all_users)
        return
