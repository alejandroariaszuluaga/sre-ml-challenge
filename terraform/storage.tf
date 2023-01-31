# Cloud Storage bucket where the Cloud Function's code and Logistic Regression model will be stored
resource "google_storage_bucket" "function_bucket" {
    name     = "${var.project_resource_id}-function"
    location = var.region
}
