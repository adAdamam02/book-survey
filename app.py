import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


# List of fiction genres
FICTION_GENRES = [
    "Action",
    "Adventure",
    "Comedy",
    "Crime",
    "Fantasy",
    "Historical",
    "Horror",
    "Mystery",
    "Romance",
    "Satire",
    "Science fiction",
    "Cyberpunk",
    "Thriller",
    "Other"
]

# List of nonfiction genres
NONFICTION_GENRES = [
    "Academic",
    "Biography",
    "Creative nonfiction",
    "Essay",
    "Journalistic writing",
    "Obituary",
    "Reference work",
    "Self-help",
    "Travel",
    "True crime"
]


@app.route("/form", methods=["GET"])
def get_form():

    # List of types of books: either fiction or nonfiction
    TYPES = [
        "Fiction",
        "Nonfiction"
    ]

    # Renders form.html, passing in FICTION_GENRES, NONFICTION_GENRES, and TYPES.
    return render_template("form.html", fiction_genres=FICTION_GENRES, nonfiction_genres=NONFICTION_GENRES, types=TYPES)


@app.route("/form", methods=["POST"])
def post_form():

    # Gets value for nome
    name = request.form.get('name')

    # Renders error.html if there is no name provided
    if not name:
        return render_template("error.html", message="You must include your name!")

    # Gets value for book
    book = request.form.get('book')

    # Makes sure user inputted book
    if not book:
        return render_template("error.html", message="You must include your favorite book!")

    # Gets value for type
    book_type = request.form.get('type')

    # Makes sure that user inputtedd a value for type
    if not book_type:
        return render_template("error.html", message="You must include whether your book is fiction or nonfiction!")

    # Creates a list that will store the book's genres
    genres = []

    # gets all of the genres from the user if the type was fiction
    if book_type == "Fiction":
        for genre in FICTION_GENRES:
            if request.form.get(genre):
                genres.append(genre)
    # gets all the genres from the user if the type was nonfiction
    else:
        for genre in NONFICTION_GENRES:
            if request.form.get(genre):
                genres.append(genre)

    # Makes sure that the user inputted at least one genre
    if len(genres) == 0:
        return render_template("error.html", message="You must include the genre(s) of your book!")

    # Creates a dictionary called info which stores the information that the user inputted in the form
    info = {
        "name": name,
        "book": book,
        "type": book_type,
        "genres": genres
    }

    # Writes info into survey.csv, storing the user's input
    with open("survey.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "book", "type", "genres"])
        writer.writerow(info)

    # redirects to sheets
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():

    # Creates a list called rows that will store rows from survey.csv
    rows = []

    # Opens survey.csv as a DictReader
    with open("survey.csv") as file:
        reader = csv.DictReader(file)

        # Gets the genres from row["genres"]; they had been stored as a list-string
        for row in reader:
            genres = row["genres"][2:len(row["genres"]) - 2].split("', '")

            # Sets row["Genres"] to genres, the list
            row["genres"] = genres

            # Appends the new row to rows
            rows.append(row)

    # Renders sheet.html, passing in rows
    return render_template("sheet.html", rows=rows)
