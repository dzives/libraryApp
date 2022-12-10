class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    firstName = db.Column(db.String(50), unique=False, nullable=False)
    lastName = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(192), unique=False, nullable=False)
    address = db.Column(db.String(100), unique=False, nullable=False)
    phoneNumber = db.Column(db.String(13), unique=True, nullable=False)

    def __repr__(self):
        return f"<Pouzivatel {self.firstName} {self.lastName} ({self.id})>"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50), unique=False, nullable=False)
    lastName = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return f"<Autor {self.firstName} {self.lastName} ({self.id})>"


class Title(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=False, nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    numberOfPages = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref="titles", lazy=True)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publisher.id"))
    publisher = db.relationship("Publisher", backref="titles", lazy=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre", backref="titles", lazy=True)
    yearOfPublishment = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Titul {self.name} (ISBN:{self.isbn})>"


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="ratings", lazy=True)
    title_id = db.Column(db.Integer, db.ForeignKey("title.id"))
    title = db.relationship("Title", backref="ratings", lazy=True)

    def __repr__(self):
        return f"<Hodnotenie {self.user.username} na knihu {self.title.name} ({self.id})>"


class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return f"<Vydavatelstvo {self.name} ({self.id})>"


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Zaner {self.name} ({self.id})>"


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey("title.id"))
    title = db.relationship("Title", backref="title", lazy=True)
    condition = db.Column(db.String(20), unique=False, nullable=True)

    def __repr__(self):
        return f"<Kniha {self.title.name} ({self.id})>"


class Rentals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    book = db.relationship("Book", backref="rentals", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref="rentals", lazy=True)
    dateOfBorrowing = db.Column(db.Date, default=datetime.date.today)
    dateOfReturn = db.Column(db.Date, nullable=False)
    returned = db.Column(db.Boolean, nullable=False)
    reminder = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Pozicka knihy {(self.book.title.name)} uzivatela {self.user.username}>"
