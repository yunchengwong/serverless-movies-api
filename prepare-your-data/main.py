from google.cloud import storage, firestore
import json
import urllib.request
from typing import List


BUCKET = "symmetrical-acorn-bucket"

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
    """Uploads a object to the bucket."""
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
        f"File {source_file_name} uploaded as {destination_blob_name}."
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

    print(f"Bucket {bucket_name} is now publicly readable")


"""Find movie data or create it and store it in your cloud NoSQL db."""

# https://cloud.google.com/firestore/docs/create-database-server-client-library#firestore_setup_dataset_pt1-python
def upload_doc(movie):
    """Uploads a document to the collection."""
    # document_name = movie['title']
    # document_data_in_dict = movie

    db = firestore.Client()
    doc_ref = db.collection("movies").document(movie['title'])
    doc_ref.set(movie)

    print(
        f'Document {movie["title"]} uploaded to collection "movies".'
    )