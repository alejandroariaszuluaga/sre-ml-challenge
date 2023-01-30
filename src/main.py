import sklearn
import pickle5 as pickle
# from google.cloud import storage

# storage_client = storage.Client()

def handler(request):
    """Background Cloud Function to be triggered by Cloud Storage.
       This generic function logs relevant data when a file is changed.
    Args:
        event (dict):  The dictionary with data specific to this type of event.
                       The `data` field contains a description of the event in
                       the Cloud Storage `object` format described here:
                       https://cloud.google.com/storage/docs/json_api/v1/objects#resource
        context (google.cloud.functions.Context): Metadata of triggering event.
    Returns:
        None; the output is written to Stackdriver Logging
    """

    print("Running CF...")
    request_data = request.form
    print(f"This was the received form-data: {request_data}")

    # bucket_name = "mytestsproject-375819-input" # <--- Replace by environment var
    # storage_client = storage.Client()
    # blobs = storage_client.list_blobs(bucket_name)
    # # Note: The call returns a response only when the iterator is consumed.
    # for blob in blobs:
    #     print(blob.name)



    # with open('serialized.pkl', 'rb') as f:
    #     data = pickle.load(f)



    return { 'message': request_data }
