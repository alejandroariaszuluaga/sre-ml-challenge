# Add model object to bucket
resource "google_storage_bucket_object" "model" {
    source = "../model-files/pickle_model.pkl"
    name   = "pickle_model.pkl"
    bucket = google_storage_bucket.function_bucket.name
}
