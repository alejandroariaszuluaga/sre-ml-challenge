resource "google_storage_bucket" "ml-model-bucket" {
  name          = "sre-challenge-ml-models"
  location      = "US"
  force_destroy = true
}
