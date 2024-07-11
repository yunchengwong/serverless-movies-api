"""
Example Data Model:
[
    {
        "title": "Inception",
        "releaseYear": "2010",
        "genre": "Science Fiction, Action",
        "coverUrl": "https://example.com/inception.jpg"
     },
    {
        "title": "The Shawshank Redemption",
        "releaseYear": "1994",
        "genre": "Drama, Crime",
        "coverUrl": "https://example.com/shawshank-redemption.jpg"
    },
    {
        "title": "The Dark Knight",
        "releaseYear": "2008",
        "genre": "Action, Crime, Drama",
        "coverUrl": "https://example.com/dark-knight.jpg"
    }
]
"""

import json
from google.cloud import firestore


# Initialize Firestore
db = firestore.Client(project="my-project-id")


# Example data
class Movie:
    def __init__(self, title, releaseYear, genre=[], coverUrl=""):
        self.title = title
        self.releaseYear = releaseYear
        self.genre = genre
        self.coverUrl = coverUrl
    
    def to_dict(self):
        return {
            "title": self.title,
            "releaseYear": self.releaseYear,
            "genre": self.genre,
            "coverUrl": self.coverUrl
        }

movies_ref = db.collection("movies")
movies_ref.set(
    Movie("Inception", "2010", ["Science Fiction", "Action"], "https://example.com/inception.jpg").to_dict()
)
movies_ref.set(
    Movie("The Shawshank Redemption", "1994", ["Drama", "Crime"], "https://example.com/shawshank-redemption.jpg").to_dict()
)
movies_ref.set(
    Movie("The Dark Knight", "2008", ["Action", "Crime", "Drama"], "https://example.com/dark-knight.jpg").to_dict()
)


# Get a document

movies = movies_ref.stream()

for movie in movies:
    print(f"{movie.id} => {movie.to_dict()}")
