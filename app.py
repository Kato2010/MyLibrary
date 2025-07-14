from ext import app
from routes import home, login, logout, signup, edit_user, delete_user, book, quiz, add_book, edit_book, delete_book,buy_book, buy_book_money, add_coins, downloads, profile

app.run(debug=True, host='0.0.0.0')
