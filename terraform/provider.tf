terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
  }
  backend "local" {}
}

provider "google" {
#   credentials = file("../../terraform-keys/mytestsproject-375819-752ffdd00eb0.json") # Since I already set this up, it might be enough to uncomment this

  project = var.project_resource_id
  region  = var.region
}

# # # # # Might prefer to do this here # # # # #
# resource "google_project_service" "service" {
#   for_each = toset([
#     "storage.googleapis.com"
#     # "compute.googleapis.com",
#     # "appengine.googleapis.com",
#     # "appengineflex.googleapis.com",
#     # "cloudbuild.googleapis.com"
#   ])

#   service            = each.key

#   project            = var.project_resource_id
#   disable_on_destroy = false
# }
