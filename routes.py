from flask import Flask, render_template, redirect, flash, request, send_from_directory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
from ext import app, db
from forms import RegisterForm, EditUserForm, LoginForm, AddBookForm, EditBookForm, QuizForm
from models import User, Book, Quiz

UPLOAD_FOLDER = path.join(app.root_path, "static")
DOWNLOAD_FOLDER = path.join(app.root_path, "downloads")


@app.route("/")
def home():
    users = User.query.all()
    wignebi = Book.query.all()
    return render_template("index.html", users=users, books=wignebi)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if not user:
            flash("This account does not exist")
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(f"/profile/{user.id}")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        file = form.profile_image.data

        new_user = User(username=form.username.data,
                        password=generate_password_hash(form.password.data),
                        gender=form.gender.data,
                        birthday=form.birthday.data,
                        country=form.country.data,
                        profile_image=file.filename,
                        coins=100,
                        role="user",
                        owned_books="")

        db.session.add(new_user)
        db.session.commit()

        file.save(path.join(UPLOAD_FOLDER, file.filename))

        return redirect("/login")

    return render_template("signup.html", form=form)


@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    form = EditUserForm(username=user.username,
                        password=user.password,
                        gender=user.gender,
                        birthday=user.birthday,
                        country=user.country,
                        profile_image=user.profile_image)

    if form.validate_on_submit():
        file = form.profile_image.data

        user.username = form.username.data
        user.password = form.password.data
        user.gender = form.gender.data
        user.birthday = form.birthday.data
        user.country = form.country.data
        user.profile_image = file.filename

        db.session.commit()

        file.save(path.join(UPLOAD_FOLDER, file.filename))

        return redirect(f"/profile/{user.id}")

    return render_template("edit_user.html", form=form)


@app.route("/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route("/books/<int:book_id>")
def book(book_id):
    wigni = Book.query.get(book_id)
    if current_user.is_authenticated:
        owned = current_user.owned_books.split("#")
        old_quiz = Quiz.query.filter(Quiz.user_id == current_user.id, Quiz.book_id == wigni.id, Quiz.q_id == "4").first()

        if str(book_id) in owned :
            book_owned = True

        else:
            book_owned = False

        if not old_quiz and str(book_id) in owned :
            quiz_passed = False

        else:
            quiz_passed = True
        return render_template("book_info.html", informacia=wigni, quiz_passed=quiz_passed, book_owned=book_owned)
    else:
        return render_template("book_info.html", informacia=wigni, quiz_passed=False, book_owned=True)


@app.route("/quiz/<int:book_id>/<int:q_id>", methods=["GET", "POST"])
@login_required
def quiz(book_id, q_id):
    answers = []
    score = 0
    wigni = Book.query.get(book_id)
    form = QuizForm()
    questions = wigni.questions.split("#")
    pasuxebi = wigni.answers.split("#")
    if form.validate_on_submit():
        new_quiz = Quiz(user_id= current_user.id,
                        book_id=book_id,
                        q_id=q_id,
                        user_answer=form.answer.data)

        db.session.add(new_quiz)
        db.session.commit()

        return redirect(f"/quiz/{wigni.id}/{q_id + 1}")
    if q_id <= 4:
        if q_id == 0:
            score = 0
            old_results = Quiz.query.filter( Quiz.user_id == current_user.id, Quiz.book_id == wigni.id).all()
            for old_result in old_results:
                db.session.delete(old_result)
            db.session.commit()
        for pasuxi in pasuxebi:
            answers.append(pasuxi.split("$"))
        for answer_id, answer in enumerate(answers[q_id]):
            form.answer.choices.append((answer_id+1, answer))
        if q_id >= 4:
            form.submit.label.text = "finish"
        return render_template("quiz.html", informacia=wigni, question=questions[q_id], answers=answers[q_id], q_id=q_id + 1, form=form)
    else:
        user_answers = []
        result = Quiz.query.filter( Quiz.user_id == current_user.id, Quiz.book_id == wigni.id).all()
        if result:
            for entry in result:
                user_answers.append(entry.user_answer)
        correct = wigni.correct_answers.split("#")
        answer_id = 0
        for user_answer in user_answers:
            if user_answer == correct[answer_id]:
                score += 1
            answer_id += 1
        user = User.query.get(current_user.id)
        coins_add = 0
        if score == 3 or score == 4:
            coins_add = 25
            user.coins = user.coins + coins_add
        elif score == 5:
            coins_add = 50
            user.coins = user.coins + coins_add
        db.session.commit()
        return render_template("finish.html", informacia=wigni, q_id=q_id + 1, form=form, score=score, coins_add=coins_add)


@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    if current_user.role == "admin":
        form = AddBookForm()
        if form.validate_on_submit():
            file = form.book_image.data
            pdf = form.book_pdf.data


            new_book = Book(name=form.book_name.data,
                            author=form.book_author.data,
                            description=form.book_description.data,
                            price=form.book_price.data,
                            price_in_coins=form.book_price_in_coins.data,
                            img=file.filename,
                            pdf = pdf.filename,
                            questions=form.book_question1.data + "#" + \
                                      form.book_question2.data + "#" + \
                                      form.book_question3.data + "#" + \
                                      form.book_question4.data + "#" + \
                                      form.book_question5.data + "#",

                            answers=form.book_answer11.data + "$" + \
                                      form.book_answer12.data + "$" + \
                                      form.book_answer13.data + "$" + \
                                      form.book_answer14.data + "#" + \
                                      form.book_answer21.data + "$" + \
                                      form.book_answer22.data + "$" + \
                                      form.book_answer23.data + "$" + \
                                      form.book_answer24.data + "#" + \
                                      form.book_answer31.data + "$" + \
                                      form.book_answer32.data + "$" + \
                                      form.book_answer33.data + "$" + \
                                      form.book_answer34.data + "#" + \
                                      form.book_answer41.data + "$" + \
                                      form.book_answer42.data + "$" + \
                                      form.book_answer43.data + "$" + \
                                      form.book_answer44.data + "#" + \
                                      form.book_answer51.data + "$" + \
                                      form.book_answer52.data + "$" + \
                                      form.book_answer53.data + "$" + \
                                      form.book_answer54.data + "#",

                            correct_answers=form.correct_answer1.data + "#" + \
                                      form.correct_answer2.data + "#" + \
                                      form.correct_answer3.data + "#" + \
                                      form.correct_answer4.data + "#" + \
                                      form.correct_answer5.data + "#")

            db.session.add(new_book)
            db.session.commit()

            file.save(path.join(UPLOAD_FOLDER, file.filename))
            pdf.save(path.join(DOWNLOAD_FOLDER, pdf.filename))


            return redirect(f"/books/{new_book.id}")

        return render_template("add_book.html", form=form)

    else:
        return redirect("/")


@app.route("/edit_book/<int:book_id>", methods=["GET", "POST"])
@login_required
def edit_book(book_id):
    wigni = Book.query.get(book_id)
    if current_user.role == "admin":
        form = EditBookForm(book_name=wigni.name,
                            book_author=wigni.author,
                            book_description=wigni.description,
                            book_price=wigni.price,
                            book_price_in_coins=wigni.price_in_coins,
                            book_image=wigni.img,
                            book_pdf=wigni.pdf,

                            book_question1=wigni.questions.split("#")[0],
                            book_answer11=wigni.answers.split("#")[0].split("$")[0],
                            book_answer12=wigni.answers.split("#")[0].split("$")[1],
                            book_answer13=wigni.answers.split("#")[0].split("$")[2],
                            book_answer14=wigni.answers.split("#")[0].split("$")[3],
                            correct_answer1=wigni.correct_answers.split("#")[0],

                            book_question2=wigni.questions.split("#")[1],
                            book_answer21=wigni.answers.split("#")[1].split("$")[0],
                            book_answer22=wigni.answers.split("#")[1].split("$")[1],
                            book_answer23=wigni.answers.split("#")[1].split("$")[2],
                            book_answer24=wigni.answers.split("#")[1].split("$")[3],
                            correct_answer2=wigni.correct_answers.split("#")[1],

                            book_question3=wigni.questions.split("#")[2],
                            book_answer31=wigni.answers.split("#")[2].split("$")[0],
                            book_answer32=wigni.answers.split("#")[2].split("$")[1],
                            book_answer33=wigni.answers.split("#")[2].split("$")[2],
                            book_answer34=wigni.answers.split("#")[2].split("$")[3],
                            correct_answer3=wigni.correct_answers.split("#")[2],

                            book_question4=wigni.questions.split("#")[3],
                            book_answer41=wigni.answers.split("#")[3].split("$")[0],
                            book_answer42=wigni.answers.split("#")[3].split("$")[1],
                            book_answer43=wigni.answers.split("#")[3].split("$")[2],
                            book_answer44=wigni.answers.split("#")[3].split("$")[3],
                            correct_answer4=wigni.correct_answers.split("#")[3],

                            book_question5=wigni.questions.split("#")[4],
                            book_answer51=wigni.answers.split("#")[4].split("$")[0],
                            book_answer52=wigni.answers.split("#")[4].split("$")[1],
                            book_answer53=wigni.answers.split("#")[4].split("$")[2],
                            book_answer54=wigni.answers.split("#")[4].split("$")[3],
                            correct_answer5=wigni.correct_answers.split("#")[4] )

        if form.validate_on_submit():
            file = form.book_image.data
            pdf = form.book_pdf.data

            wigni.name = form.book_name.data
            wigni.author = form.book_author.data
            wigni.description = form.book_description.data
            wigni.price = form.book_price.data
            wigni.price_in_coins = form.book_price_in_coins.data
            wigni.img = file.filename
            wigni.pdf = pdf.filename

            wigni.questions = form.book_question1.data + "#" + \
                        form.book_question2.data + "#" + \
                        form.book_question3.data + "#" + \
                        form.book_question4.data + "#" + \
                        form.book_question5.data + "#"

            wigni.answers = form.book_answer11.data + "$" + \
                      form.book_answer12.data + "$" + \
                      form.book_answer13.data + "$" + \
                      form.book_answer14.data + "#" + \
                      form.book_answer21.data + "$" + \
                      form.book_answer22.data + "$" + \
                      form.book_answer23.data + "$" + \
                      form.book_answer24.data + "#" + \
                      form.book_answer31.data + "$" + \
                      form.book_answer32.data + "$" + \
                      form.book_answer33.data + "$" + \
                      form.book_answer34.data + "#" + \
                      form.book_answer41.data + "$" + \
                      form.book_answer42.data + "$" + \
                      form.book_answer43.data + "$" + \
                      form.book_answer44.data + "#" + \
                      form.book_answer51.data + "$" + \
                      form.book_answer52.data + "$" + \
                      form.book_answer53.data + "$" + \
                      form.book_answer54.data + "#"

            wigni.correct_answers = form.correct_answer1.data + "#" + \
                              form.correct_answer2.data + "#" + \
                              form.correct_answer3.data + "#" + \
                              form.correct_answer4.data + "#" + \
                              form.correct_answer5.data + "#"

            db.session.commit()

            file.save(path.join(UPLOAD_FOLDER, file.filename))
            pdf.save(path.join(DOWNLOAD_FOLDER, pdf.filename))

            return redirect(f"/books/{wigni.id}")

        return render_template("edit_book.html", form=form)

    else:
        return redirect(f"/books/{wigni.id}")



@app.route("/delete_book/<int:book_id>")
@login_required
def delete_book(book_id):
    if current_user.role == "admin":
        wigni = Book.query.get(book_id)
        db.session.delete(wigni)
        db.session.commit()

    return redirect("/")


@app.route("/buy_book/<int:book_id>")
@login_required
def buy_book(book_id):
    wigni = Book.query.get(book_id)
    user = User.query.get(current_user.id)
    if user.coins >= wigni.price_in_coins:
        user.coins = user.coins - wigni.price_in_coins
        if user.owned_books:
            user.owned_books += "#" + str(book_id)
        else:
            user.owned_books+= str(book_id)
        db.session.commit()
    else:
        flash("Error: You don't have enough coins!", "alert-danger")

    return redirect(f"/books/{book_id}")


@app.route("/buy_book_money/<int:book_id>")
@login_required
def buy_book_money(book_id):

    flash("Error: You cant buy a book with real money yet", "alert-warning")

    return redirect(f"/books/{book_id}")


@app.route("/add_coins")
@login_required
def add_coins():
    if current_user.role == "admin":
        user = User.query.get(current_user.id)
        user.coins = user.coins + 100
        db.session.commit()

    return redirect(request.referrer)


@app.route("/downloads/<int:book_id>")
def downloads(book_id):
    wigni = Book.query.get(book_id)
    owned = current_user.owned_books.split("#")
    if current_user.is_authenticated:

        if str(book_id) in owned or current_user.role == "admin":
            print(book_id)
            return send_from_directory("downloads/", wigni.pdf, as_attachment=True)


@app.route("/profile/<int:user_id>")
@login_required
def profile(user_id):
    user = User.query.get(user_id)
    return render_template("profile.html", userinfo=user)
