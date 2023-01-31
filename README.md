# sre-ml-challenge
This repository will store all files related to the SRE Challenge for Latam Airlines. This project can be deployed by authenticating to GCP by running installing Google Cloud SDK and Terraform (this work was developed using TF v1.3.7), and then running `gcloud init`, followed by `terraform apply`.

This will deploy a Cloud Storage bucket where both the Cloud Function's code (zip package), and the `pickle_model.pkl` model file will be stored. It'll also make the function available through an endpoint with the form `https://<gcp-region>-<gcp-project-id>.cloudfunctions.net/<function-name>`. This function is configured to handle POST requests with a form-based payload, see below an example on how to trigger this function via `curl`, using (an already `gcloud` authenticated) shell commands:

```console
foo@bar:~$ curl -X POST -d 'x=[0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]' -H "Authorization: bearer $(gcloud auth print-identity-token)" https://us-central1-mytestsproject-375819.cloudfunctions.net/function-run-pickle-model
{"model_prediction":"[1]","received_data":{"x":"[0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]"}}
```

# Project Structure

    .
    ├── model-files            # Provided files related to code challenge
    ├── src                    # Cloud Function source files
    ├── terraform              # GCP IaC Terraform files
    └── README.md

## Cloud Function Source
CF code ZIP package will be created by Terraform and it'll include dependencies specified in the `requirements.txt` file.

## Model Files
Here, all the files provided by the creators of this challenge were stored, while some tests where developed in the `.ipynb`, these can be ignored. The file `pickle_model.pkl` that is uploaded to a Cloud Storage bucket also lives here.

## Terraform
All `.tf` and GCP IaC-related files live here. All information related to the Terraform State will not be committed to GitHub for security purposes. It is important to note that the `provider.tf` file may be modified in order to store the `.tfstate` remotely, this good practice is highly recommended for Production workloads.
**IMPORTANT:** when getting started to build this infrastructure, the user must have an existing project with billing enabled, as well as the corresponding GCP resources' APIs enabled (these are not enabled by default, Terraform will prompt with an error that provides corresponding links where the user may enable these APIs). The `terraform.tfvars` variables' values should be replaced by the corresponding project ID and the GCP region where these resources should be created.

