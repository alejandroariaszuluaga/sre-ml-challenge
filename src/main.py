import ast
from google.cloud import storage
import logging
import os
import pickle5 as pickle
import traceback

storage_client = storage.Client()
BUCKET_NAME = os.environ.get('BUCKET_NAME')
MODEL_FILENAME = os.environ.get('MODEL_FILENAME')
LOG_LEVEL = os.environ.get('LOG_LEVEL')

log_level_map = {
	'DEBUG': logging.DEBUG,
	'INFO': logging.INFO,
	'WARNING': logging.WARNING,
	'ERROR': logging.ERROR,
	'CRITICAL': logging.CRITICAL,
}

logging.basicConfig(level=log_level_map[LOG_LEVEL])

def handler(request):
    """Cloud Function to be triggered by an http request.
       This function is configured to handle POST requests with a form-payload
       numeric array (x=[0,0,1,0,1,1,...]), which will then be the input to a
       Logistic Regression model that will return one of the classes `0` or `1`
       as part of a JSON response.
       In case a Python exception is raised, its message will be returned as part
       of a JSON response.
    Args:
        request: dictionary holding POST request form-payload, it must contain
        the numeric array as the value for an key named `x`.
    Returns:
        result: dictionary with corresponding model output/error message with
                Python exception content.
    """

    try:
        logging.info("Running CF...")
        request_data = request.form
        logging.debug(f"This was the received form-data: {request_data}")
        x = ast.literal_eval(request_data['x']) # We receive a string object with a list definition so we need to convert it to an actual list object

        # Getting model Blob from bucket
        bucket = storage_client.bucket(BUCKET_NAME)
        model = bucket.blob(MODEL_FILENAME)
        logging.debug(f"Pickle model file `{model.name}` has been loaded")

        # Convert to string and load model using pickle5
        pickle_in = model.download_as_string()
        model = pickle.loads(pickle_in)

        # Use model to predict data
        result = model.predict( [x] ) # Passing x between brackets b/c model.predict receives a list of arrays/or a 2D array
        logging.info(f"Prediction finished correctly")
        logging.debug(f"Model predicted the class: {result}")

        return { 'received_data': request_data, 'model_prediction': str(result) }
    except Exception as e:
        logging.error(f"There was an error when handling the request: {traceback.format_exc()}")
        return { "error_message": f"Python exception: {e}. Check CF logs for more details." }
