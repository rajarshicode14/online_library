from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models.user import User
from .models.library import Library
from .models.books import Books
from .models.owned_books import OwnedBooks
from .models.userType import UserType
from website import db
from flask_login import login_user, logout_user, login_required, current_user
import os
from werkzeug.security import generate_password_hash, check_password_hash


views = Blueprint("views", __name__)


# Home entry
@views.route('/',  methods=['GET', 'POST'])
def index():
    return render_template('index.html', user=current_user)


# Library home page
@views.route('/library_home',  methods=['GET', 'POST'])
@login_required
def library_home():

    if current_user.type == 2:
        return redirect(url_for("views.index"))

    lib = Library.query.filter_by(user_type=current_user.id).first()
    books = Books.query.filter_by(library_id=lib.id)
    return render_template('library_home.html', books=books, user=current_user)


# Library signup
@views.route('/library_sign_up', methods=['GET', 'POST'])
def library_sign_up():

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        library_name = data['library_name']
        address = data['address']
        postal_code = data['postal_code']
        contact_no = data['contact_no'],
        email = data['email']
        registration_no = data['registration_no_lib']
        password = data['password']
        confirm_password = data['confirm_password']

        lib = UserType(type=1)
        db.session.add(lib)
        db.session.flush()
        db.session.refresh(lib)

        new_lib = Library(
            library_name=library_name,
            address=address,
            postal_code=postal_code,
            contact_no=contact_no,
            email=email,
            registration_no=registration_no,
            password=generate_password_hash(password, method="sha256"),
            user_type=lib.id
        )
        db.session.commit()
        login_user(lib)

        db.session.add(new_lib)
        db.session.commit()

        flash("Account successfully created", category="success")
        return redirect(url_for('views.library_home'))
    return render_template("library_sign_up.html", user=current_user)

# User signup
@views.route('/user_sign_up', methods=['GET', 'POST'])
def user_sign_up():

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        full_name = data['full_name'],
        email = data['email'],
        contact_no = data['contact_no'],
        country = data['country'],
        password = data['password']
        confirm_password = data['confirm_password']

        user = UserType(type=2)
        db.session.add(user)
        db.session.flush()
        db.session.refresh(user)

        new_user = User(
            full_name=full_name,
            email=email,
            contact_no=contact_no,
            country=country,
            password=generate_password_hash(password, method="sha256"),
            user_type=user.id
        )

        db.session.commit()
        login_user(user)

        db.session.add(new_user)
        db.session.commit()
        flash("Account successfully created", category="success")

        return redirect(url_for('views.all_books'))

    return render_template("user_sign_up.html", user=current_user)

# Library login
@views.route('/library_log_in', methods=['GET', 'POST'])
def library_log_in():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        email = data['email']
        password = data['password']

        user = Library.query.filter_by(email=email).first()
        to_login = UserType.query.filter_by(id=user.user_type).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", category="success")
                login_user(to_login)

                return redirect(url_for('views.library_home'))
            else:
                flash("Invalid Password", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template('library_log_in.html', user=current_user)


# User login
@views.route('/user_log_in', methods=['GET', 'POST'])
def user_log_in():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        to_login = UserType.query.filter_by(id=user.user_type).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in Successfully!", category="success")
                login_user(to_login)
                return redirect(url_for('views.all_books'))
            else:
                flash("Invalid Password", category="error")
        else:
            flash("Email does not exist", category="error")

    return render_template('user_log_in.html', user=current_user)


# Logout
@views.route('/logout')
@login_required
def logout():

    logout_user()
    flash("You are successfully logged out", category="success")
    return redirect(url_for("views.index"))

# Add books
@views.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():

    if current_user.type == 2:
        return redirect(url_for("views.index"))
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        title = data["title"]
        author = data["author"]
        publisher = data["publisher"]
        edition = data["edition"]
        library_name = data["library_name"]
        genre = data["genre"]
        image = request.files["image"]
        pdf = request.files["pdf"]

        new_book = Books(
            title=title,
            author=author,
            publisher=publisher,
            edition=edition,
            library_name=library_name,
            genre=genre,
            issued_count=0,
            library_id=current_user.id,
        )

        db.session.add(new_book)
        db.session.flush()
        db.session.refresh(new_book)

        base_dir = os.path.dirname(os.path.abspath(__file__))

        img_path = os.path.join(
            base_dir, 'static/data/img', f"{new_book.id}.jpg")
        pdf_path = os.path.join(
            base_dir, 'static/data/pdf', f"{new_book.id}.pdf")

        image.save(img_path)
        pdf.save(pdf_path)

        db.session.commit()
        flash("Book added successfully", category="success")

        return redirect(url_for('views.library_home'))

    return render_template("add_book.html", user=current_user)

# All available books
@views.route('/all_books', methods=['GET', 'POST'])
@login_required
def all_books():

    books = Books.query.all()

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        user = User.query.filter_by(user_type=current_user.id).first()

        new_owned_book = OwnedBooks(
            user_id=user.id,
            book_id=data['book_id'],
            is_read=False
        )
        db.session.add(new_owned_book)
        db.session.commit()
        flash("Book successfully added to reading list", category="success")
        return redirect(url_for('views.currently_reading'))

    return render_template("all_available_books.html", user=current_user, books=books)


# Currently reading
@views.route('/currently_reading', methods=['GET', 'POST'])
@login_required
def currently_reading():

    if current_user.type == 1:
        return redirect(url_for("views.index"))

    user = User.query.filter_by(user_type=current_user.id).first()

    data = OwnedBooks.query.filter(OwnedBooks.user_id == user.id).filter(
        OwnedBooks.is_read == False).all()

    items_list = [item.book_id for item in data]

    items = Books.query.filter(Books.id.in_(items_list)).all()

    if request.method == "POST":
        if 'read' in request.form:
            id = request.form['book_id1']
            file_name = f"{id}.pdf"
            return render_template("read.html", file_name=file_name, user=current_user)

        if 'mark_read' in request.form:

            data = request.form.to_dict(flat=True)
            id = data['book_id2']
            user = User.query.filter_by(user_type=current_user.id).first()
            update = OwnedBooks.query.filter(
                OwnedBooks.user_id == user.id, OwnedBooks.book_id == id).first()
            update.is_read = True
            db.session.commit()
            flash("Book successfully added to finished list", category="success")
            return redirect(url_for('views.finished_reading'))

    return render_template("currently_reading.html", user=current_user, books=items)

# Finished reading
@views.route('/finished_reading', methods=['GET', 'POST'])
@login_required
def finished_reading():
    if current_user.type == 1:
        return redirect(url_for("views.index"))
    user = User.query.filter_by(user_type=current_user.id).first()

    data = OwnedBooks.query.filter(OwnedBooks.user_id == user.id).filter(
        OwnedBooks.is_read == True).all()

    items_list = [item.book_id for item in data]

    items = Books.query.filter(Books.id.in_(items_list)).all()

    if request.method == "POST":
        data = request.form.to_dict(flat=True)
        id = data['book_id']
        user = User.query.filter_by(user_type=current_user.id).first()
        update = OwnedBooks.query.filter(
            OwnedBooks.user_id == user.id, OwnedBooks.book_id == id).first()
        update.is_read = False
        db.session.commit()
        flash("Book successfully added to reading list", category="success")
        return redirect(url_for('views.currently_reading'))

    return render_template("finished_reading.html", user=current_user, books=items)
