import logging

import azure.functions as func


def main(req: func.HttpRequest, connectionInfo) -> func.HttpResponse:
    logging.info('negotiate: fonction déclenchée')
    return func.HttpResponse(connectionInfo)
