# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "source" {
    type        = "zip"
    source_dir  = "../src"
    output_path = "/tmp/function.zip"
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "zip" {
    source       = data.archive_file.source.output_path
    content_type = "application/zip"

    # Append to the MD5 checksum of the files's content
    # to force the zip to be updated as soon as a change occurs
    name         = "src-${data.archive_file.source.output_md5}.zip"
    bucket       = google_storage_bucket.function_bucket.name
}

# Create the Cloud function triggered by an HTTP request
resource "google_cloudfunctions_function" "function" {
    name                  = "function-run-pickle-model"
    runtime               = "python39"

    # Get the source code of the cloud function as a Zip compression
    source_archive_bucket = google_storage_bucket.function_bucket.name
    source_archive_object = google_storage_bucket_object.zip.name

    # Must match the function name in the cloud function `main.py` source code
    entry_point           = "handler"

    trigger_http          = true

    environment_variables = {
        LOG_LEVEL = "DEBUG"
        BUCKET_NAME = google_storage_bucket.function_bucket.name
        MODEL_FILENAME = google_storage_bucket_object.model.name
    }
}

# Permissions to access bucket objects where the ML model will be uploaded
resource "google_project_iam_member" "function_bucket_reader" {
  project = var.project_resource_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_cloudfunctions_function.function.service_account_email}"
}
