import json
import requests

class NerApi:
    def __init__(self, url, api_key):
        self.endpoint = url
        self.api_key = api_key
        self.header = {"Authorization": f"Bearer {self.api_key}"}

    """This function works faster with async calls."""

    def query(self, payload: str):
        try:
            data = json.dumps(payload)
            response = requests.request("POST", self.endpoint, headers=self.header, data=data)
            response = json.loads(response.content.decode("utf-8"))

            dicts = dict()
            for token in response:
                klas = token['entity_group']
                if klas in dicts:
                    # to append if word is cutted in two without space append without space while adding
                    dicts[klas][0] += token["word"]  if dicts[klas][1] == token["start"] else token["word"] + "  "
                    dicts[klas][1] = token["end"]
                else:
                    dicts[klas] = [token["word"] + "  ", token["end"]] 

            for key in dicts.keys():
                dicts[key] = [dicts[key][0].replace(" ##", "").replace("##", "").replace("## ", "").strip(), dicts[key][1]]

            res_dict = {k: v[0] for k, v in dicts.items()}
            return {
            'full_text': payload,
             'address': self.concat_address(res_dict),
             'ws':self.calculate_score(res_dict),
            }
        except Exception as e:
            return {
            'full_text': payload,
             'address': "",
             'ws':0,
            }
    
    def concat_address(self, result):
        address_str = ""
        for key, value in result.items():
            if value != "":
                if key == "il":
                    address_str = address_str + " " + value + " "
                if key == "ilce":
                    address_str = address_str + " " + value + " "
                if key == "mahalle":
                    address_str = address_str + " " + value + " "
                if key == "sokak":
                    address_str = address_str + " " + value + " "
                if key == "Apartman/Site":
                    address_str = address_str + " " + value + " "
                if key == "dis kapi no":
                    address_str = address_str + " " + value + " "
                if key == "ic kapi no":
                    address_str = address_str + " " + value + " "
        return address_str

    def calculate_score(self, result):
        weighted_score = 0

        if result.get("il"):
            weighted_score += 5
        if result.get("ilce"):
            weighted_score += 5
        if result.get("mahalle"):
            weighted_score += 4
        if result.get("sokak"):
            weighted_score += 3
        if result.get("Apartman/Site"):
            weighted_score += 3
        if result.get("dis kapi no"):
            weighted_score += 1
        if result.get("ic kapi no"):
            weighted_score += 1

        return weighted_score / (5 + 5 + 4 + 3 + 3 + 1 + 1)