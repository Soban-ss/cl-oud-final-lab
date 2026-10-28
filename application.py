

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

application = Flask(__name__)

application.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///bookstore.db"
)
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)

# Book database model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# READ: Display all books
@application.route("/")
def home():
    books = db.session.execute(
        db.select(Book).order_by(Book.id.desc())
    ).scalars().all()
    return render_template("index.html", books=books)

# CREATE: Add a new book
@application.route("/add", methods=["POST"])
def add_book():
    book = Book(
        title=request.form["title"],
        author=request.form["author"],
        category=request.form["category"],
        price=float(request.form["price"]),
        quantity=int(request.form["quantity"])
    )
    db.session.add(book)
    db.session.commit()
    return redirect(url_for("home"))

# UPDATE: Edit existing book
@application.route("/update/<int:id>", methods=["POST"])
def update_book(id):
    book = db.get_or_404(Book, id)
    book.title = request.form["title"]
    book.author = request.form["author"]
    book.category = request.form["category"]
    book.price = float(request.form["price"])
    book.quantity = int(request.form["quantity"])
    db.session.commit()
    return redirect(url_for("home"))

# DELETE: Remove a book
@application.route("/delete/<int:id>", methods=["POST"])
def delete_book(id):
    book = db.get_or_404(Book, id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))

with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run(debug=True)
