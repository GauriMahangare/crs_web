from storages.backends.gcloud import GoogleCloudStorage


class StaticGoogleCloudStorage(GoogleCloudStorage):
    location = "static"
    default_acl = "publicRead"


class MediaGoogleCloudStorage(GoogleCloudStorage):
    location = "media"
    file_overwrite = False
