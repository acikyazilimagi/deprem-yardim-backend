import os
import json
import requests
class NerApi():

    def __init__(self,url,api_key):
        self.endpoint = "https://api-inference.huggingface.co/models/deprem-ml/deprem-ner"
        self.api_key = api_key
        self.header ={"Authorization": f"Bearer {self.api_key}"}

    """This function works faster with async calls."""
    def query(self,payload: str):
        data = json.dumps(payload)
        response = requests.request("POST", self.api_key, headers=self.header, data=data)
        response = json.loads(response.content.decode("utf-8"))

        dicts = dict()
        for token in response:
            klas = token['entity_group']
            if klas in dicts:
                # to append if word is cutted in two without space append without space while adding
                dicts[klas][0] += " " + token["word"] if dicts[klas][1] == token["start"] else token["word"]
                dicts[klas][1] = token["end"]
            else:
                dicts[klas] = [token["word"], token["end"]]
        return {k: v[0] for k, v in dicts.items()}