import logging
import requests, uuid, json, os

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('translate: fonction déclenchée')
    # Récupération des paramètres pour la traduction
    req_body = req.get_json()
    target_language = req_body["dest_lang"]
    text_to_translate = req_body["text"]
    source_language = req_body["source_lang"] if "source_lang" in req_body.keys() else "en"

    # Endpoint de l'API
    endpoint = "https://api.cognitive.microsofttranslator.com/translate"
    # Clé de l'API
    key = os.getenv("TRANSLATOR_KEY")
    # Région de l'API
    location = os.getenv("TRANSLATOR_REGION")

    # Paramètres de la requête
    params = {
        'api-version': '3.0',
        'from': source_language,
        'to': [target_language]
    }

    # En-têtes de la requête
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text_to_translate
    }]

    response = requests.post(endpoint, params=params, headers=headers, json=body)
    response_str = json.dumps(response.json(), sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': '))
    logging.info(response_str)
    return func.HttpResponse(response_str)
