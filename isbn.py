import requests
import json
from app import *


def book_info(isbn):
    url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    response = requests.get(url)
    book_data = json.loads(response.text)
    book_info = {
        "name": book_data[f'ISBN:{isbn}']['title'],
        "author": book_data[f'ISBN:{isbn}']['authors'][0]['name'],
        "publisher": book_data[f'ISBN:{isbn}']['publishers'][0]['name'],
        "number_pages": book_data[f'ISBN:{isbn}']['number_of_pages'],
        "year": book_data[f'ISBN:{isbn}']['publish_date'],
        "isbn": isbn
    }
    return book_info


def add_book(book_info):
    pub = Publisher.query.filter(Publisher.name.like(f"%{book_info['publisher']}%")).first()
    aut = Author.query.filter(Author.name.like(f"%{book_info['author']}%")).first()
    if not pub:
        pub = Publisher(name=book_info['publisher'])
        db.session.add(pub)
    if not aut:
        aut = Author(name=book_info['author'])
        db.session.add(aut)
    db.session.add(Title(name=book_info['name'], isbn=book_info['isbn'], numberOfPages=book_info['number_pages'], author=aut, publisher=pub, yearOfPublishment=book_info['year']))
    db.session.commit()


if __name__ == "__main__":
    # HP books
    add_book(book_info("9780747532743"))
    add_book(book_info("9781408810552"))
    add_book(book_info("9780439136365"))
    add_book(book_info("9780747546245"))
    add_book(book_info("9780747551003"))
    add_book(book_info("9780747581420"))
    add_book(book_info("9780747591054"))
    # RANDOM
    add_book(book_info("9780571241231"))
    add_book(book_info("9780007331802"))
    add_book(book_info("9781529010084"))
