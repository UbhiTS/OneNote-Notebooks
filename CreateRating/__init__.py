import logging
import json
import requests
import uuid
import os
import azure.functions as func

from datetime import datetime


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    message = req.get_json()
    message["id"] = str(uuid.uuid4())
    message["timestamp"] = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')

    # Validations
    if message["rating"] not in range(0, 5):
       return func.HttpResponse("This rating not in range from 0 .. 5", status_code=400)

    response = requests.get(os.getenv('KeyVaultGetUserUrl') + message["userId"])
    if response.status_code == 400:
        return func.HttpResponse("This user does not exist", status_code=400)

    response = requests.get(os.getenv('KeyVaultGetProductUrl') + message["productId"])
    if response.status_code == 400:
        return func.HttpResponse("This product does not exist", status_code=400)

    item = json.dumps(message)

    doc.set(func.Document.from_json(item))

    return func.HttpResponse(item, status_code=200)
    


