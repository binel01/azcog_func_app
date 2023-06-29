import logging
import json

import azure.functions as func


def main(documents: func.DocumentList, signalRMessages: func.Out[str]) -> str:
    logging.info("pushImageDescription: fonction déclenchée")
    # Récupération de la liste de documents sous forme de chaîne de caractères
    doc_list = []
    for doc in documents:
        doc_list.append(json.dumps(doc.to_json()))

    # Envoi du document aux clients via SignalR
    signalRMessages.set(json.dumps({
        'target': 'newMessage',
        'arguments': doc_list
    }))
    logging.info(f"pushImageDescription: message SignalRMessage envoyé aux clients")
