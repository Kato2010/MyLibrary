from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileSize
from wtforms.fields import StringField, PasswordField, DateField, RadioField, SelectField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, length, equal_to



class RegisterForm(FlaskForm):
    username = StringField("Enter your username", validators=[DataRequired()])

    password = PasswordField("Enter password", validators=[DataRequired(), length(min=8, max=20)])

    repeat_password = PasswordField("Repeat password",
                                    validators=[DataRequired(), equal_to("password", message="Passwords do not match")])

    birthday = DateField("Enter your birthday", validators=[DataRequired()])

    gender = RadioField("Choose gender", choices=["Male", "Female", "Other"], validators=[DataRequired()])

    country = SelectField("Choose country", choices=["Georgia", "USA", "UK"], validators=[DataRequired()])

    profile_image = FileField("Upload profile picture",
                              validators=[FileSize(1024 * 1024), FileRequired(), FileAllowed(["jpg", "png", "jpeg"])])

    submit = SubmitField("Sign Up")


class EditUserForm(FlaskForm):
    username = StringField("Enter your username", validators=[DataRequired()])

    password = PasswordField("Enter new password", validators=[DataRequired(), length(min=8, max=20)])

    repeat_password = PasswordField("Repeat new password",
                                    validators=[DataRequired(), equal_to("password", message="Passwords do not match")])

    birthday = DateField("Enter your birthday", validators=[DataRequired()])

    gender = RadioField("Choose gender", choices=["Male", "Female", "Other"], validators=[DataRequired()])

    country = SelectField("Choose country", choices=["Georgia", "USA", "UK"], validators=[DataRequired()])

    profile_image = FileField("Upload profile picture",
                              validators=[FileSize(1024 * 1024), FileRequired(), FileAllowed(["jpg", "png", "jpeg"])])

    submit = SubmitField("Save")


class LoginForm(FlaskForm):
    username = StringField("Enter your username", validators=[DataRequired()])

    password = PasswordField("Enter password", validators=[DataRequired(), length(min=3, max=20)])

    submit = SubmitField("Login")


class AddBookForm(FlaskForm):
    book_name = StringField("Enter name of a book", validators=[DataRequired()])
    book_author = StringField("Enter author of the book", validators=[DataRequired()])
    book_description = TextAreaField("Enter description of a book", validators=[DataRequired()])
    book_price = IntegerField("Enter price of a book", validators=[DataRequired()])
    book_price_in_coins = IntegerField("Enter price of a book in coins", validators=[DataRequired()])
    book_image = FileField("Upload picture of a book",
                           validators=[FileSize(1024 * 1024), FileRequired(), FileAllowed(["jpg", "png", "jpeg"])])
    book_pdf = FileField("Upload PDF of a book",
                           validators=[FileSize(1024 * 1024 * 10), FileRequired(), FileAllowed(["pdf"])])
    book_question1 = TextAreaField("Enter first question", validators=[DataRequired()])
    book_answer11 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer12 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer13 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer14 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer1 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                  validators=[DataRequired()])
    book_question2 = TextAreaField("Enter second question", validators=[DataRequired()])
    book_answer21 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer22 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer23 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer24 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer2 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                  validators=[DataRequired()])
    book_question3 = TextAreaField("Enter third question", validators=[DataRequired()])
    book_answer31 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer32 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer33 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer34 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer3 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                  validators=[DataRequired()])
    book_question4 = TextAreaField("Enter fourth question", validators=[DataRequired()])
    book_answer41 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer42 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer43 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer44 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer4 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                  validators=[DataRequired()])
    book_question5 = TextAreaField("Enter fifth question", validators=[DataRequired()])
    book_answer51 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer52 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer53 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer54 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer5 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                  validators=[DataRequired()])

    submit = SubmitField("create")

class EditBookForm(FlaskForm):
    book_name = StringField("Enter name of a book", validators=[DataRequired()])
    book_author = StringField("Enter author of the book", validators=[DataRequired()])
    book_description = TextAreaField("Enter description of a book", validators=[DataRequired()])
    book_price = IntegerField("Enter price of a book", validators=[DataRequired()])
    book_price_in_coins = IntegerField("Enter price of a book in coins", validators=[DataRequired()])
    book_image = FileField("Upload picture of a book",
                               validators=[FileSize(1024 * 1024), FileRequired(), FileAllowed(["jpg", "png", "jpeg"])])
    book_pdf = FileField("Upload PDF of a book",
                         validators=[FileSize(1024 * 1024 * 10), FileRequired(), FileAllowed(["pdf"])])
    book_question1 = TextAreaField("Enter first question", validators=[DataRequired()])
    book_answer11 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer12 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer13 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer14 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer1 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                      validators=[DataRequired()])
    book_question2 = TextAreaField("Enter second question", validators=[DataRequired()])
    book_answer21 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer22 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer23 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer24 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer2 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                      validators=[DataRequired()])
    book_question3 = TextAreaField("Enter third question", validators=[DataRequired()])
    book_answer31 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer32 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer33 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer34 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer3 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                      validators=[DataRequired()])
    book_question4 = TextAreaField("Enter fourth question", validators=[DataRequired()])
    book_answer41 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer42 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer43 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer44 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer4 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                      validators=[DataRequired()])
    book_question5 = TextAreaField("Enter fifth question", validators=[DataRequired()])
    book_answer51 = TextAreaField("Enter first answer option", validators=[DataRequired()])
    book_answer52 = TextAreaField("Enter second answer option", validators=[DataRequired()])
    book_answer53 = TextAreaField("Enter third answer option", validators=[DataRequired()])
    book_answer54 = TextAreaField("Enter fourth answer option", validators=[DataRequired()])
    correct_answer5 = SelectField("Choose correct answer", choices=["1", "2", "3", "4"],
                                      validators=[DataRequired()])

    submit = SubmitField("Save")


class QuizForm(FlaskForm):
    answer = RadioField("quiz_answers", choices=[], validators=[DataRequired()], validate_choice=False)

    submit = SubmitField("next")





