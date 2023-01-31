import ast
from google.cloud import storage
import os
import pickle5 as pickle
import sklearn
import traceback

storage_client = storage.Client()
BUCKET_NAME = os.environ.get('BUCKET_NAME')
MODEL_FILENAME = os.environ.get('MODEL_FILENAME')

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

    try:
        print("Running CF...")
        request_data = request.form
        print(f"This was the received form-data: {request_data}")
        x = ast.literal_eval(request_data['x']) # We receive a string object with a list definition so we need to convert it to an actual list object

        # Getting model Blob from bucket
        bucket = storage_client.bucket(BUCKET_NAME)
        model = bucket.blob(MODEL_FILENAME)

        # Convert to string and load model using pickle5
        pickle_in = model.download_as_string()
        model = pickle.loads(pickle_in)

        # Use model to predict data
        result = model.predict( [x] ) # Passing x between brackets b/c model.predict receives a list of arrays/or a 2D array

        return { 'received_data': request_data, 'model_prediction': str(result) }
    except Exception as e:
        print(traceback.format_exc())
        return { "error_message": f"Python exception: {e}. Check CF logs for more details." }
