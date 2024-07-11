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
from google.cloud import firestore


db = firestore.Client()

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
movies_ref.add(
    Movie(
        "Inception", 2010,  ["Science", "Fiction", "Action"], "https://example.com/inception.jpg"
    ).to_dict()
)
movies_ref.add(
    Movie(
        "The Shawshank Redemption", 1994, ["Drama", "Crime"], "https://example.com/shawshank-redemption.jpg"
    ).to_dict()
)
movies_ref.add(
    Movie(
        "The Dark Knight", 2008, ["Action", "Drama", "Crime"], "https://example.com/dark-knight.jpg"
    ).to_dict()
)

movies = movies_ref.stream()

for movie in movies:
    print(f"{movie.id} => {movie.to_dict()}")

"""
WARNING: All log messages before absl::InitializeLog() is called are written to STDERR
I0000 00:00:1720696414.445065   10934 config.cc:230] gRPC experiments enabled: call_status_override_on_cancellation, event_engine_dns, event_engine_listener, http2_stats_fix, monitoring_experiment, pick_first_new, trace_record_callops, work_serializer_clears_time_cache, work_serializer_dispatch
I0000 00:00:1720696414.445295   10934 ev_epoll1_linux.cc:125] grpc epoll fd: 3
I0000 00:00:1720696414.461098   10976 socket_utils_common_posix.cc:382] TCP_USER_TIMEOUT is available. TCP_USER_TIMEOUT will be used thereafter
253VuJ5BQoxY1pukR8P6 => {'coverUrl': 'https://example.com/shawshank-redemption.jpg', 'title': 'The Shawshank Redemption', 'releaseYear': 1994, 'genre': ['Drama', 'Crime']}
nczy0AcyDI2F6QvzaYWI => {'coverUrl': 'https://example.com/inception.jpg', 'title': 'Inception', 'releaseYear': 2010, 'genre': ['Science', 'Fiction', 'Action']}
ugWb7YQgjqgO5eqzfIn0 => {'coverUrl': 'https://example.com/dark-knight.jpg', 'title': 'The Dark Knight', 'releaseYear': 2008, 'genre': ['Action', 'Drama', 'Crime']}
I0000 00:00:1720696417.854417   10976 tcp_posix.cc:809] IOMGR endpoint shutdown
"""