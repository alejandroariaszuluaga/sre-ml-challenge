resource "google_storage_bucket" "function_bucket" {
    name     = "${var.project_resource_id}-function"
    location = var.region
}
