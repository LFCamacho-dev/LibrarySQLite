from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)

# CREATE DATABASE

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/main_db.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CREATE TABLE
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.VARCHAR(80), unique=True, nullable=False)
    author = db.Column(db.VARCHAR(120), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


# first step, in the python console, don't run in the script :)
# db.create_all()

#region CRUD COMMANDS
# CREATE RECORD
# new_book = Book(id=1, title="Harry Potter", author="J. K. Rowling", rating=9.3)
# db.session.add(new_book)
# db.session.commit()

# READ ALL RECORDS
# all_books = session.query(Book).all()

# READ A PARTICULAR RECORD BY QUERY
# book = Book.query.filter_by(title="Harry Potter").first()

# UPDATE A PARTICULAR RECORD BY QUERY
# book_to_update = Book.query.filter_by(title="Harry Potter").first()
# book_to_update.title = "Harry Potter and the Chamber of Secrets"
# db.session.commit()

# UPDATE A RECORD BY PRIMARY KEY
# book_id = 1
# book_to_update = Book.query.get(book_id)
# book_to_update.title = "Harry Potter and the Goblet of Fire"
# db.session.commit()

# DELETE A PARTICULAR RECORD BY PRIMARY KEY
# book_id = 1
# book_to_delete = Book.query.get(book_id)
# db.session.delete(book_to_delete)
# db.session.commit()
#endregion


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        # Adding a new book entry to the db
        db.session.add(
            Book(
                title=request.form['title'],
                author=request.form['author'],
                rating=request.form['rating']
            )
        )
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    if request.method == 'POST':
        Book.query.get(request.form['book_id']).rating = request.form['new_rating']
        db.session.commit()
        return redirect(url_for('home'))
    book = Book.query.get(request.args.get('book_id'))
    return render_template('edit_rating.html', book=book)


@app.route("/delete")
def delete_book():
    db.session.delete(Book.query.get(request.args.get('book_id')))
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
