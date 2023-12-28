import requests
import json, pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import pandas as pd

encoding_key = "	aJI3VsNcr69ZG2FR5dx8EilBOhjmaX1EiM2d9IxjjbqSIBGliVc7U2hT3%2BbNdINTAIQFTzdMNfpD%2FaemMvFyVQ%3D%3D"


def json2pandas(url, params):
    r = urlopen(Request(url + '?' + urlencode(params)))
    json_api = r.read().decode('utf-8')
    json_file = json.loads(json_api)
    df = pd.json_normalize(json_file['response']['body']['items']['item'])
    return df