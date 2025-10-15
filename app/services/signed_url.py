from google.cloud import storage
import datetime
import os


def generate_signed_url(blob_name):
    """Generates a v4 signed URL for downloading a blob."""
    bucket_name = os.getenv("BUCKET_NAME")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Define el tiempo de expiración de la URL
    expiration_time = datetime.timedelta(minutes=15)

    url = blob.generate_signed_url(
        version="v4",
        expiration=expiration_time,
        method="GET",  # Permite descargar el archivo
    )

    print(f"La URL firmada es: {url}")
    return url
