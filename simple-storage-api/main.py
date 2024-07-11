from google.cloud import storage


def authenticate_implicit_with_adc():
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()
    print("Buckets:")
    for bucket in buckets:
        print(bucket.name)
    print("Listed all storage buckets.")

authenticate_implicit_with_adc()