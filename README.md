# sre-ml-challenge
This repository will store all files related to the SRE Challenge for Latam Airlines. This project can be deployed by following the instructions below:

1. Install Google Cloud CLI (https://cloud.google.com/sdk/docs/install)
1. Install Terraform CLI (https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
1. Authenticate via the CLI to your Google Cloud account: `gcloud init`
1. Create a Google Cloud project and set Terraform up to use current login, here's a way to do that using the CLI:
```console
PROJECT_ID=myproject-whatever-whatever-whatever
gcloud projects create $PROJECT_ID --set-as-default

gcloud auth application-default login
```

1. Enable billing for that project
    1. Go into the cloud console
    1. Go into billing -> Account Management
    1. Select the My Projects tab
    1. Click on the Actions button for the new project and Change Billing
    1. Select the proper billing account and save the change

1. Enable APIs that this project will use, you can do that from the cloud console too, the APIs that should be enabled are the following:
    1. Cloud Functions API
    1. Cloud Logging API
    1. Cloud Pub/Sub API
    1. Cloud Build API

1. Finally, create Terraform infrastructure:
    1. `terraform init`
    1. `terraform plan`
    1. Check the previous command's output and run `terraform apply --auto-approve`


This will deploy a Cloud Storage bucket where both the Cloud Function's code (zip package), and the `pickle_model.pkl` model file will be stored. It'll also make the function available through an endpoint with the form `https://<gcp-region>-<gcp-project-id>.cloudfunctions.net/<function-name>`. This function is configured to handle POST requests with a form-based payload, see below an example on how to trigger this function via `curl`, using (an already `gcloud` authenticated) shell commands, as well as a sample response from it:

```console
foo@bar:~$ curl -X POST -d 'x=[0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]' -H "Authorization: bearer $(gcloud auth print-identity-token)" https://us-central1-mytestsproject-375819.cloudfunctions.net/function-run-pickle-model

> {"model_prediction":"[1]","received_data":{"x":"[0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0]"}}

```

# Project Structure

    .
    ├── load-tests             # Load tests script (.lua)
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

# Load Tests
The load-tests directory holds a simple `.lua` script that was developed to be used by [wrk - a HTTP benchmarking tool](https://github.com/wg/wrk), the `<gcloud-bearer-token>` should be replaced by the output of `gcloud auth print-identity-token` before running the load test.

The results that were obtained by getting >50000 requests (this was a requirement defined by the challenge, so I just tried different load test configuration until the required number of requests were hit under the time interval) in 45 seconds can be observed (and can be reproduced by installing the `wrk` tool and running the `.lua` script in this repositor) below:

```console
foo@bar:~$ ./wrk -t 3 -c 190 -d 45s -s scripts/cf-pickle.lua --latency https://us-central1-mytestsproject-375819.cloudfunctions.net/function-run-pickle-model

Running 45s test @ https://us-central1-mytestsproject-375819.cloudfunctions.net/function-run-pickle-model
  3 threads and 190 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   197.60ms  205.99ms   1.98s    90.96%
    Req/Sec   428.41    173.99   640.00     75.99%
  Latency Distribution
     50%  126.57ms
     75%  176.18ms
     90%  364.74ms
     99%    1.20s 
  51033 requests in 45.08s, 27.27MB read
  Socket errors: connect 0, read 0, write 0, timeout 91
Requests/sec:   1131.97
Transfer/sec:    619.33KB
```

## Load Test Parameters
The selected parameters, as well as their influence in each load test, were the following:

    * 3 threads: this is proportionally related to how many simultaneous requests can be sent to the application. The more complex the load test workflow is, the longer each thread will finish its task and will become available for another run. How many threads can be run depends on the system's memory and CPU in which it's run. Each thread may be considered as a user hitting the application from an independent machine.
    * 190 connections: this parameter indicates how many HTTP connections each thread will handle. Depending on how long the load test workflow takes to finish, each http request will finish and consequently the thread will become available to run another request.
    * Duration of 45 seconds: this indicates how long each thread will remain open and hitting the application.

# Improving Performance
There are several possible upgrades that may be implemented to improve performance:

1. Cache ML pickle model: currently, this model is loaded directly from a Cloud Storage bucket, a caching method that is able to deliver this object faster would improve this loading process.
1. Increase Cloud Function's memory resources.
1. Increase the Cloud Function autoscaling minimum instances in response to the request load received.
1. Have regional redundancy, by deploying different functions into variant regions.


# Authorization Mechanisms
In order to be able to call this function's endpoint, the use needs to use an authorized IAM user.

## Performance Implications
This specific kind of authentication increases the latency of the application at two fronts: first, generating the bearer token depends on the user's connection to the authorizer (in this case, the response time of `gcloud auth`); second, the backend (the Cloud Function) authorization token's processing time, which mostly depends on how Google Cloud Functions handle each request whenever it gets the `Authorization` header.

### Bearer Token
At the moment of writing this, only the main owner of this function would be able to generate the corresponding bearer token that this endpoint requires. This can be modified in order to give permissions to a different IAM user, such that other users may have access to the API as well.

### IP Access Restrictions
By adding a network configuration and a number of firewall rules that define which CIDRs are allowed to invoke the function, traffic from certain IPs can be restricted.

### VPC Access
Also, a VPC can be setup so that the function is able to interact only with elements inside the VPC.

# SLOs and SLIs
The main SLOs and SLIs that are relevant for this scenario, according to my own concepts and opinion, are:

1. API Availability of 99.95%:
    * Request success rate.
    * Uptime: since this is a serverless and stateless architecture, this metrics would greatly be related to Google Cloud Functions Service's SLA.
1. API Latency P90 response time shorter than 400ms (based on load tests' results):
    * Response time (P90): this metric is more reliable and accurate to reality, than simple average metric.
1. Resource Utilization lower than 256MB:
    * Memory: this one is important to keep around, in case the ML model is replaced by a heavier one, it might get to the point where the function's resources are not enough, and should be increased accordingly.
