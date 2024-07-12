from google.cloud import storage, firestore
import json
import urllib.request
from typing import List


BUCKET = "moviesapi-bucket-[project]"

"""Store movie cover images of each movie in cloud storage."""

# https://cloud.google.com/storage/docs/reference/libraries#client-libraries-usage-python
# https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-client_libraries
def create_bucket(bucket_name):
    """Create a bucket with default configurations."""
    # bucket_name = "my-new-bucket"

    storage_client = storage.Client()

    bucket = storage_client.create_bucket(bucket_name)

    print(
        f"Bucket {bucket.name} created."
    )

    return bucket


# https://stackoverflow.com/questions/25412119/uploading-an-image-from-an-external-link-to-google-cloud-storage-using-google-ap
# https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "moviesapi-bucket"
    # source_file_name = movie['coverUrl']
    # destination_blob_name = movie['title'] + ".jpg"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # blob.upload_from_filename(source_file_name)
    try:
        with urllib.request.urlopen(source_file_name) as response:
            # check if URL contains an image
            info = response.info()
            if(info.get_content_type().startswith("image")):
                blob.upload_from_string(response.read(), content_type=info.get_content_type())
                print("Uploaded image from: " + source_file_name)
            else:
                print("Could not upload image. No image data type in URL")
    except Exception:
        print('Could not upload image. Generic exception: ' + traceback.format_exc())

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )


# https://cloud.google.com/storage/docs/access-control/making-data-public#storage-make-object-public-python
def set_bucket_public_iam(
    bucket_name: str = "your-bucket-name",
    members: List[str] = ["allUsers"],
):
    """Set a public IAM Policy to bucket"""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append(
        {"role": "roles/storage.objectViewer", "members": members}
    )

    bucket.set_iam_policy(policy)

    print(f"Bucket {bucket.name} is now publicly readable")


# "Public access URL: https://storage.googleapis.com/$BUCKET/$OBJECT"

create_bucket(BUCKET)

with open('example_data.json') as f:
    movies = json.load(f)

for movie in movies:
    movie['id'] = movie['title'].replace(" ", "").lower() + movie['releaseYear']
    upload_blob(movie['coverUrl'], movie['id'] + ".jpg")
    movie['coverUrl'] = f"https://storage.googleapis.com/{BUCKET}/{movie['id']}.jpg"

with open('processed_data.json', 'w') as f:
    json.dump(movies, f, indent=4)

set_bucket_public_iam(BUCKET)


"""Find movie data or create it and store it in your cloud NoSQL db."""

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