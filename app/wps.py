import requests
import json


def consultar_contrato(data):

    url = 'https://wps-login.herokuapp.com/login'

    request = requests.post(url=url, json=data)

    return request
