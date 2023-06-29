import json
import logging
import os

import azure.functions as func


# Clé de Azure Cognitive Services
VISION_SUBS_KEY = os.environ["VISION_SUBS_KEY"]
# Point d'accès à Azure Cognitive Services
VISION_ENDPOINT = os.environ["VISION_ENDPOINT"]

def main(event: func.EventGridEvent, doc:func.Out[func.Document]):
    """
    ================================================
    1. Récupération de l'url de l'image uploadée
    ================================================
    """
    logging.info("getUploadedImage: function triggered")
    logging.info(event)
    # Récupération de l'url de l'image uploadée dans Azure Blob Storage
    image_url = event["data"]["url"]

    """
    =======================================================
    2. Analyse de l'image
    =======================================================
    """
    # Récupération du client Computer Vision
    vision_client = ComputerVisionClient(VISION_ENDPOINT, CognitiveServicesCredentials(VISION_SUBS_KEY))
    # Génération de la description
    image_description:ImageDescription = vision_client.describe_image(image_url)
    if (len(description.captions) == 0):
        logging.info("Pas de description détectée")
    else:
        for caption in description.captions:
            logging.info("Description: '{}' avec la probabilité: {}".format(caption.text, caption.confidence))

    """
    =======================================================
    3. Sauvegarde de la description dans la base de données
    =======================================================
    """
    document = {
        "image_url": image_url,
        "image_description": image_description,
    }

    doc.set(func.Document.from_json(document))
    logging.info(f"Le document a bien été enregistré dans la base de donnée {document}")
