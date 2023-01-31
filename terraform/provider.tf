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
  project = var.project_resource_id
  region  = var.region
}
