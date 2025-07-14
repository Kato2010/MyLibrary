from ext import app, db
from models import User, Book, Quiz
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

users = [{"username": "kato", "password": "Furina13", "birthday" : date(2010, 8, 9), "gender": "Female", "country": "Georgia",
          "profile_image": "katopfp.jpg", "coins" : 1000, "role" : "admin"},
         {"username": "lizi", "password": "Navia999", "birthday": date(2010, 6, 9), "gender": "Female", "country": "Georgia",
          "profile_image": "lizipfp.jpg", "coins": 100, "role": "user"}
         ]

books =[{"name": "Silmarilion", "author": "J. R. R. Tolkien", "img": "silmarilion.jpg", "price": 15.79, "price_in_coins" : 50, "pdf" : "silmarilion.pdf", "description": "The Silmarillion is the history of the War of the Exiled Elves against the Enemy, which all takes place in the North-west of the world (Middle-earth). Several tales of victory and tragedy are caught up in it; but it ends with catastrophe, and the passing of the Ancient World, the world of the long First Age.",
         "questions" : "Who created the Silmarils?#What is the name of the world created by Eru Ilúvatar?#What was Melkor’s name after he was cast out and became evil?#Which two trees gave light to the world before the creation of the Sun and Moon?#What is the fate of the Silmarils at the end of the First Age?",
         "answers" : "Sauron$Melkor$Fëanor$Thingol#Arda$Aman$Beleriand$Númenor#Anárion$Morgoth$Círdan$Ulmo#Celeborn and Galadriel$Telperion and Laurelin$Andúril and Narsil$Lórien and Vána#They are all returned to Valinor$They are destroyed by Sauron$They are lost: one in the sky, one in the sea, one in the earth$They are given to Frodo for safekeeping",
         "correct_answers" : "3#1#2#2#3" },
    {"name": "Crime and Punishment", "author": "Fyodor Dostoevsky", "img": "crime.jpg", "price": 15.79, "price_in_coins" : 50, "pdf" : "crime_and_punishment.pdf", "description": "Crime and Punishment is a story of an individual's journey through a battle of conscience for his crime borne out of the conditions of his time. Aimless and without money, Rodion Romanovich Raskolnikov wanders the city, concocting a plan to kill the pawnbroker, Alyona Ivanovna.",
     "questions": "What is the name of the protagonist of the novel?#What crime does Raskolnikov commit?#What is Raskolnikov’s main philosophical belief that justifies his crime?#Who is Sonya Marmeladov?#How does the novel end?",
     "answers": "Arkady Ivanovich$Rodion Romanovich Raskolnikov$Dmitri Karamazov$Pavel Svidrigailov#Theft from a church$Forgery$Murder of a pawnbroker$Arson# All people are equal under God$Some individuals have the right to transgress moral laws for a greater purpose$True justice comes from the law$Suffering leads to salvation#Raskolnikov’s sister$A detective$A poor woman forced into prostitution who becomes Raskolnikov’s confidante$The pawnbroker’s niece#Raskolnikov escapes to America$Raskolnikov commits suicide$Raskolnikov is executed$Raskolnikov confesses and is sent to Siberia",
     "correct_answers": "2#3#2#3#4"},
    {"name": "Dead Souls", "author": "Nikolai Gogol", "img": "dead.jpg", "price": 15.79, "price_in_coins" : 50, "pdf" : "dead_souls.pdf", "description": "The plot of Dead Souls follows protagonist Chichikov as he carries out a scheme to purchase the rights of deceased serfs, or dead souls, from the Imperial Russian aristocracy. Chichikov hopes to levy the equity of his dead souls to secure a bank loan that will make him rich.",
     "questions": "Who is the main character of Dead Souls?#What is Chichikov trying to buy throughout the novel?#Why does Chichikov want to acquire “dead souls”#What genre is Dead Souls best categorized as?#How do most of the landowners Chichikov visits react to his request to buy dead souls?",
     "answers": "Pavel Ivanovich Chichikov$Ivan Ilyich$Alexei Vronsky$Dmitri Gurov#Horses$Government positions$Dead serfs (souls) still listed in the census$Antique artifacts#To create a ghost army$To use them as collateral to acquire land and wealth$To free their spirits from purgatory$To help the government identify census errors#Romantic poetry$Historical epic$Satirical novel$Gothic horror#They are horrified and report him$They are suspicious but eventually agree$They enthusiastically support him$They refuse to speak to him",
     "correct_answers": "1#3#2#3#2"},
    {"name": "No Longer Human", "author": "Osamu Dazai", "img": "nolongerhuman.jpg", "price": 15.79, "price_in_coins" : 50, "pdf" : "no_longer_human.pdf", "description": "It tells the story of a troubled man incapable of revealing his true self to others, and who, instead, maintains a façade of hollow jocularity, later turning to a life of alcoholism before his final disappearance. The original title translates as 'Disqualified as a human being' or 'A failed human'.",
     "questions": "What is the name of the protagonist in No Longer Human?#What coping mechanism does Yozo Oba use throughout much of his life to hide his true feelings?#What major theme is central to No Longer Human?#What type of narrative structure does the novel use?#What ultimately happens to Yozo Oba by the end of the novel?",
     "answers": "Yozo Oba$Kunikida Doppo$Yukio Mishima$Naoji#Excessive reading$Drawing caricatures$Humor and clownish behavior$Aggression and violence#War and political rebellion$Exploration and discovery$Alienation and loss of identity$Justice and moral law#A detective’s journal$A series of letters written to a friend$A third-person omniscient narrator$A series of notebooks (diaries) from the protagonist#He finds redemption and becomes a teacher$He is sent to a mental institution and considered “no longer human”$He flees to another country$He writes a bestselling novel and becomes famous",
     "correct_answers": "1#3#3#4#2"},
    {"name": "At the Mountains of Madness", "author": "H. P. Lovecraft", "img": "atthemountains.jpg", "price": 15.79, "price_in_coins" : 50, "pdf" : "at_the_mountains_of_madness.pdf", "description": "The story details the events of a disastrous expedition to Antarctica in September 1930, and what is found there by a group of explorers led by the narrator, Dr. William Dyer of Miskatonic University.",
     "questions": "Who is the narrator of At the Mountains of Madness?#What is the purpose of the Miskatonic University expedition to Antarctica?#What ancient alien race does the expedition discover evidence of?#What horrifying discovery do the explorers make about the Elder Things’ creations?#Why does Dr. Dyer later warn others not to continue Antarctic exploration?",
     "answers": "Professor Armitage$Dr. William Dyer$Charles Dexter Ward$Randolph Carter#To search for alien life$To investigate meteorological phenomena$To conduct geological and scientific research$To mine for rare minerals#The Mi-Go$The Deep Ones$The Elder Things$The Great Race of Yith#They created dinosaurs$They created and were overthrown by the shoggoths$They brought humans to Earth$They built the pyramids#Because of dangerous weather patterns$To protect ancient religious secrets$Because of the terrifying and unnatural creatures discovered$To keep military powers from exploiting the land",
     "correct_answers": "2#3#3#2#3"}]

with app.app_context():
    db.drop_all()
    db.create_all()

    for user in users:
        new_user = User(
            username=user["username"],
            password=generate_password_hash(user["password"]),
            gender=user["gender"],
            country=user["country"],
            birthday=user["birthday"],
            profile_image=user["profile_image"],
            coins=user["coins"],
            role=user["role"],
            owned_books = "")

        db.session.add(new_user)
        db.session.commit()

    for book in books:
        new_book = Book(
            name=book["name"],
            author=book["author"],
            img=book["img"],
            price=book["price"],
            price_in_coins=book["price_in_coins"],
            description=book["description"],
            pdf=book["pdf"],
            questions=book["questions"],
            answers=book["answers"],
            correct_answers=book["correct_answers"])
        db.session.add(new_book)
        db.session.commit()


