import requests
import json


def consultar_contrato(data):

    url = 'http://127.0.0.1:81'

    request = requests.post(url=url, verify=False, json=data)

    return request
