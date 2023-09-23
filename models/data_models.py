from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"

    def __str__(self):
        return f"User: {self.name}"


class Movie(db.Model):
    __tablename__ = 'Movie'

    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    year = db.Column(db.String)
    rating = db.Column(db.Float)
    director = db.Column(db.String)
    poster = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return f"<Movie(id={self.movie_id}, title='{self.title}', year={self.year}, rating={self.rating})>"

    def __str__(self):
        return f"Movie: {self.title} ({self.year}), Rating: {self.rating}"


class Review(db.Model):
    __tablename__ = 'Review'

    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    review = db.Column(db.String)

    movie = db.relationship('Movie', backref='reviews', lazy=True)
    user = db.relationship('User', backref='reviews', lazy=True)

    def __repr__(self) -> str:
        return (f"Review(review_id={self.review_id}, user_id={self.user_id},"
                f" movie_id={self.movie_id}, review='{self.review}')")

    def __str__(self) -> str:
        return f"Review: {self.review_id}, {self.review}"
